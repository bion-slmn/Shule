from django.urls import path
from . import views

urlpatterns =[
    path('create-term-fees/', views.create_TermFees),
    path('make-payment/', views.make_payment),
    path('view-feepaid/', views.schoolfee_statement),
    path('view-all-feepaid/', views.schoolfee_statement_all),
    path('view-all-payments/', views.all_payments)
]