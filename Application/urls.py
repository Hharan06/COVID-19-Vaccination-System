from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('enroll',views.enroll),
    path('enrolled',views.enroll),
    path('created',views.create_account),
    path('loginsuccess',views.login_authentication,name='dashboard'),
    path('login',views.login),
    path('vaccine_appointment',views.vaccine_appointment),
    path('vaccine',views.vaccine_appointment),
    path('register',views.patients),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient_dashboard/choose/<str:name>', views.vaccine_display, name="vaccine_display"),
    path('register_patient/',views.vaccine_display),
    path('patient_information/', views.patient_information, name='patient_information'),
    path('patient_information/gethealthcare',views.patient_information),
    path('vaccine_information',views.vaccine_information,name="vaccine_information"),
    path('download_certificate',views.aadhar),
    path('aadhar',views.aadhar),
    path('patient_information/delete/<str:aadhar>',views.delete_patient),
    path('delete_vaccine/<str:vaccine_id>',views.delete_vaccine),
    path('patient_information/update/<str:aadhar>',views.update_patients),
    path('submit_update_patients',views.update_patients),
    path('update_vaccine/<str:vaccine_id>',views.update_vaccines),
    path('submit_update_vaccines',views.update_vaccines)
]
