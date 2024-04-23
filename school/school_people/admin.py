from django.contrib import admin
from .models import Profile, School, Parent, Student


# Register your models here.
admin.site.register(Profile)
admin.site.register(School)
admin.site.register(Parent)
admin.site.register(Student)