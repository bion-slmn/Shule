from django.urls import path
from . import views


urlpatterns = [
                path('sign_up/', views.sign_up),
                path('login/', views.login_user),
                path('create-school/', views.create_school),
                path('register-parent/',  views.register_parent),
                path('admit-student/', views.admit_student),
                ]