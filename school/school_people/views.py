from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.db import IntegrityError
from django.core.cache import cache
from django.contrib.auth import authenticate, logout, login
import time
from .models import School, Parent, Student
# Create your views here.


@api_view(['POST'])
def sign_up(request):
    '''
    sign up a the admin,
    '''
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    
    if not username or not password:
        return Response(
                        'Username and password must be passed',
                        status.HTTP_400_BAD_REQUEST
                        )

    try:
        user = User.objects.create_user(
                                        username=username,
                                        password=password,
                                        email=email
                                        )
        return Response(f'{user.username} created', status.HTTP_201_CREATED)
    except IntegrityError:
        return Response('User already exists', status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_user(request):
    '''
    login a user
    '''
    start = time.time()
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
                        'Username and password must be passed',
                        status.HTTP_400_BAD_REQUEST
                        )

    user = authenticate(username=username, password=password)

    if user:
        login(request, user)
        # check if the profile pic been cached
        profile_pic_url = cache.get(f'profile_pic_url_{user.id}')
        # if its database hit
        if not profile_pic_url:
            try:
                profile_pic_url = user.profile.profile_pic.url
            except Exception:
                profile_pic_url = '/media/profile_pics/default.png'
            cache.set(f'profile_pic_url_{user.id}', profile_pic_url, timeout=3600)
        print(time.time() - start)
        return Response(
                        {'name': username, 'profilePic': profile_pic_url},
                        status=status.HTTP_200_OK
                        )
    return Response(
                    'Check that password or username',
                    status=status.HTTP_404_NOT_FOUND
                    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_school(request):
    '''S
    create a school associated with the current user
    '''
    name = request.data.get('name')
    user = request.user

    if not name:
        return Response('Please add school name', status.HTTP_400_BAD_REQUEST)
    try:
        school = School.objects.create(name=name, user=user)
    except IntegrityError:
        return Response('Name already exists', status.HTTP_400_BAD_REQUEST)
    return Response({'id': school.id, 'name': name}, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_parent(request):
    '''
    regisster the parent
    '''
    fullname = request.data.get('fullName')
    phone_number = request.data.get('phoneNumber')
    email = request.data.get('email')
    related = request.data.get('relationship')
    
    
    if not fullname:
            return Response('Add fullName', status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    school = cache.get(f'user_school_{user.id}')
    if not school:
        school=user.school
        cache.set(f'user_school_{user.id}', school)


    try:
        parent, created = Parent.objects.get_or_create(
                                   full_name=fullname,
                                   phone_number=phone_number,
                                   email=email,
                                   relationship=related,
                                   school=school
                                   )
        if not created:
            return Response('Parent already exists', status.HTTP_400_BAD_REQUEST)
        return Response(
                        {'Name': fullname, 'id': parent.id},
                        status.HTTP_200_OK
                        )
    except IntegrityError:
        return Response('Try again', status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admit_student(request):
    '''
    admit a student to a school
    '''
    user = request.user
    school = user.school

    parent_id = request.data.get('parentId')
    fullname = request.data.get('fullName')
    grade = int(request.data.get('grade'))
    
    parent = Parent.objects.filter(id=parent_id).first()
    if not parent:
        return Response('parent doesnt exist', status.HTTP_400_BAD_REQUEST)

    student, created = Student.objects.get_or_create(
                                     full_name=fullname,
                                     grade=grade,
                                     school=school,
                                     parent=parent
                                     )
    # create a school fee to be paid for that student
    if not created:
        return Response('Student already admitted', status.HTTP_400_BAD_REQUEST)
    return Response(
                    {'Names':fullname.upper(), 'id': student.id},
                    status.HTTP_200_OK
                    )