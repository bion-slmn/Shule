from django.db import models
from school_people.models import Student, School
import uuid
from django.utils import timezone

class BaseModel(models.Model):
    '''
    defines a base model for other to inherit
    '''
    id = models.UUIDField('id of the object',
                          primary_key=True,
                          default=uuid.uuid4,
                          editable=False
                          )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ''' this instructs django not to create a table for this class
        '''
        abstract = True


# Create your models here.
class TermFees(BaseModel):
    '''
    defines the structure and the term of 
    '''
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    school_term = models.CharField(max_length=70, unique=True)
    fees = models.FloatField()
    start_date = models.DateField('Start of term date', default=timezone.now)
    end_date = models.DateField('end of term date', default=timezone.now)

    def __str__(self):
        return self.school_term
    


class SchoolFeePaid(BaseModel):
    '''
    defines the school fee paid by the student
    '''
    amount_paid = models.FloatField()
    balance = models.FloatField()
    termfees = models.OneToOneField(
                                    TermFees,
                                    on_delete=models.CASCADE,
                                    related_name='term'
                                    )
    student = models.ForeignKey(
                                Student,
                                on_delete=models.CASCADE)

    
    def __str__(self):
        return f'{self.student.full_name} {self.termfees.school_term} {self.balance} {self.amount_paid}'

class Payment(BaseModel):
    '''
    define how payment of fees were made, it handlle installment payments
    or one time payment
    '''
    amount = models.FloatField()
    student = models.ForeignKey(
                                Student,
                                on_delete=models.CASCADE
                                )
    payment_method = models.CharField(max_length=50)
    

    def __str__(self):
        return f'{self.student.full_name} {self.amount}'