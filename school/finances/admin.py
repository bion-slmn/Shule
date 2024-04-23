from django.contrib import admin

# Register your models here.
from .models import Payment, SchoolFeePaid, TermFees

admin.site.register(TermFees)
admin.site.register(SchoolFeePaid)
admin.site.register(Payment)
