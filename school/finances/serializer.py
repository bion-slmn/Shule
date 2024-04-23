'''
serialising django objects to python structures
'''
from .models import SchoolFeePaid, Payment
from rest_framework import serializers


class SchoolFeesSerializer(serializers.ModelSerializer):
    '''
    serialise the product model
    '''
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    student_name = serializers.SerializerMethodField()

    def get_student_name(self, obj):
        return obj.student.full_name
    
    class Meta:
        model = SchoolFeePaid
        fields =  ["created_at", "updated_at", "student_name", "amount_paid", "balance"]

class PaymentSerialiser(serializers.ModelSerializer):
    '''
    serialise the payments
    '''
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    student_name = serializers.SerializerMethodField()

    def get_student_name(self, obj):
        return obj.student.full_name

    class Meta:
        model = Payment
        fields = ["created_at", "student_name", "amount", "payment_method"]