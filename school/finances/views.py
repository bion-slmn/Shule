from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.db import IntegrityError
from django.core.cache import cache
from django.contrib.auth import authenticate, logout, login
from django.db.models import F, Prefetch
from .models import TermFees, SchoolFeePaid, Payment
from school_people.models import Student
from .serializer import SchoolFeesSerializer, PaymentSerialiser
from datetime import datetime, timedelta
from django.utils import timezone




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_TermFees(request):
    '''
    create a fees to be paid for a specific term
    '''
    user = request.user
    school = cache.get(f'user_school_{user.id}')
    if not school:
        school=user.school
        cache.set(f'user_school_{user.id}', school)
    
    school_term = request.data.get('schoolTerm')
    fees = request.data.get('schoolFees', 0.00)
    start_date = request.data.get('startDate')
    end_date = request.data.get('endDate')

    if not school_term:
        return Response('School term must be passed', status.HTTP_400_BAD_REQUEST)
    if end_date <= start_date:
        return Response('End term must be bigger start date',
                        status.HTTP_400_BAD_REQUEST)


    try:
        # a post _save signal is used to created school fee to be paid
        # for all students
        term = TermFees.objects.create(
                                        school_term=school_term,
                                        fees=fees,
                                        start_date=start_date,
                                        end_date=end_date,
                                        school=school
                                        )
        return Response({'term_id':term.id}, status.HTTP_200_OK)
    except IntegrityError:
        return Response(
                        'A term with that name already exists',
                         status.HTTP_400_BAD_REQUEST
                         )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_payment(request):
    '''
    make payment for fees for a specific student
    '''
    amount = float(request.data.get('amount'))
    payment_method = request.data.get('paymentMethod')
    student_id = request.data.get('studentId')

    # feteching school object and the school fee and term object
    student_obj = Student.objects.prefetch_related(
                    'schoolfeepaid_set').get(id=student_id)
    if not student_obj:
        return Response('Student doest exist', status.HTTP_200_OK)
    
    # create a payment
    paid = Payment.objects.create(
                            amount=amount,
                            payment_method=payment_method,
                            student=student_obj
                            )
    student_obj = Student.objects.prefetch_related(
                    'schoolfeepaid_set').get(id=student_id)

    # update the latest schoolfee paid
    fee_paid = student_obj.schoolfeepaid_set.order_by('-created_at').first()
    fee_paid.balance -= amount
    fee_paid.amount_paid += amount
    fee_paid.save()
    
    return Response({student_obj.full_name: fee_paid.balance}, status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def schoolfee_statement(request):
    '''
    view  the school fee paid  statemaent for the latest term
    '''
    student_id = request.query_params.get('studentId')

    fee_paid = cache.get(f'schoolfee_statement_{student_id}')
    # check if it cache hit
    if fee_paid:
        return Response(fee_paid, status.HTTP_200_OK)

    # if its a cache miss
    # feteching school object and the school fee and term object
    latest_fee_paid_prefetch = Prefetch(
                                        'schoolfeepaid_set',
                                        queryset=SchoolFeePaid.objects.order_by('-created_at')
                                        )

    # Use the Prefetch object in the prefetch_related call.
    student_obj = Student.objects.prefetch_related(latest_fee_paid_prefetch).get(id=student_id)
    if not student_obj:
        return Response('Student doest exist', status.HTTP_400_BAD_REQUEST)
    
    fee_paid = student_obj.schoolfeepaid_set.first()
    serial = SchoolFeesSerializer(fee_paid).data

    cache.set(f'schoolfee_statement_{student_id}', serial)
    return Response(serial, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def schoolfee_statement_all(request):
    '''
    view all the school fee paid  statemaent for the student
    '''
    student_id = request.query_params.get('studentId')
    #check if its a cache hit
    all_feespaid =  cache.get(f'schoolfee_statement_all_{student_id}')
    if all_feespaid:
        return Response(all_feespaid, status.HTTP_200_OK)
    # if its a cache miss
    # feteching school object and the school fee and term object
    student_obj = Student.objects.prefetch_related(
                    'schoolfeepaid_set').get(id=student_id)
    if not student_obj:
        return Response('Student doest exist', status.HTTP_400_BAD_REQUEST)
    fee_paid = student_obj.schoolfeepaid_set.all()
    serial_data = SchoolFeesSerializer(fee_paid, many=True).data
    cache.set(f'schoolfee_statement_all_{student_id}', serial_data )
    return Response(serial_data, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_payments(request):
    '''
    view all school feepaiyment payments for a specified student,
    for the last 3 monnths
    '''
    student_id = request.query_params.get('studentId')

    #check if it was cached
    all_payments = cache.get(f'payments_{student_id}')
    if all_payments:
        return Response(all_payments, status.HTTP_200_OK)
    
    # a cache miss
    student_obj = Student.objects.prefetch_related(
                    'payment_set').filter(id=student_id).first()
    if not student_obj:
        return Response('Student doest exist', status.HTTP_400_BAD_REQUEST)
    
    payments = student_obj.payment_set.all()[:10]
    serial = PaymentSerialiser(payments, many=True)
    all_payments = serial.data
    cache.set(f'payments_{student_id}', all_payments, timeout = 60 * 5)
    return Response(all_payments)
