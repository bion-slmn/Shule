from django.db import models
import uuid
from django.contrib.auth.models import User


# Create your models here
#create the profile of the Admin
class Profile(models.Model):
    '''
    create the profile of the admin
    '''
    user = models.OneToOneField(
                               User,
                               on_delete=models.CASCADE,
                               related_name='profile'
                               )
    phone_number = models.CharField(max_length=12, null=True)
    profile_pic = models.ImageField(
                                   upload_to='profile_pics/',
                                   null=True
                                   )

    def __str__(self):
        return self.user.username


# create school profile
class School(models.Model):
    '''
    create a school model
    '''
    id = models.UUIDField(
                          primary_key=True,
                          default=uuid.uuid4,
                          editable=False
                          )
    name = models.CharField(max_length=30, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.name

class Parent(models.Model):
    id = models.UUIDField(
                          primary_key=True,
                          default=uuid.uuid4,
                          editable=False
                          )
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    relationship = models.CharField('relationship with student',
                                    max_length=50, null=True)
    email = models.EmailField(max_length=254, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.full_name 



class Student(models.Model):
    '''
    create a model for students
    '''
    id = models.UUIDField(
                          primary_key=True,
                          default=uuid.uuid4,
                          editable=False
                          )
    full_name = models.CharField(max_length=50)
    grade = models.IntegerField('The class/grade of the student')
    parent =  models.ForeignKey(Parent, on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.full_name 