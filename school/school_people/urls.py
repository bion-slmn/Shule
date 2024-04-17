from django.urls import path
from . import views


urlpatterns = [
                path('sign_up/', views.sign_up),
                path('login/', views.login_user),
                path('create_school/', views.create_school)
                ]
