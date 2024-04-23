from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from finances.models import Student, TermFees, SchoolFeePaid


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
        '''
        when ever a user is created, a profile is created
        in the database for that user
        '''
        if created:
            profile = Profile.objects.create(user=instance)


@receiver(post_save, sender=Student)
def create_fees_to_be_paid(sender, instance, created, **kwargs):
    '''
    when ever a student a is created the school fee to be paid
    for the latest, term
    '''
    if created:
        # choose the latest term
        term = TermFees.objects.order_by('-created_at').first()
        
        if term:
            fee_to_pay = SchoolFeePaid.objects.create(
                                                    amount_paid=0.0,
                                                    balance=term.fees,
                                                    termfees=term,
                                                    student=instance
                                                    )
            print(term)
        else:
            print('No term in yet')