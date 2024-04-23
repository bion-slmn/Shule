'''
create signals so that when a new fee structure is created,
strudent of that grade will automatically have fee balance

example if a school fee 500 is created for grade 4, all students
of grade 4 will have balance
'''
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import TermFees, SchoolFeePaid


@receiver(post_save, sender=TermFees)
def create_schoolfes_to_be_paid(sender, instance, created, **kwargs):
    '''
    when a school term fee is created,
    for all students in that class a fee to be paid is
    created int database
    '''
    if created:
        school = instance.school  # schoool has a onetoone with instance
        students = school.student_set.all()
        fees = instance.fees

        '''
        all students will have the same school fees to be paid
        '''
        fees_to_b_paid = [SchoolFeePaid(
                                        amount_paid=0.0,
                                        balance=fees,
                                        termfees=instance,
                                        student=student,
                                        )
                          for student in students]
        # using bulk create
        obj = SchoolFeePaid.objects.bulk_create(fees_to_b_paid)
        print('Object created', obj)