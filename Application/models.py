from django.db import models

# Create your models here.
class HealthCareInformation(models.Model):
    name=models.CharField(max_length=100,default="")
    contact=models.CharField(max_length=20,default="")
    email=models.CharField(max_length=50,default="")
    phone=models.CharField(max_length=50,default="")
    city=models.CharField(max_length=50,default="")
    location=models.CharField(max_length=50,default="")

class Login(models.Model):
    username=models.CharField(max_length=50,default="")
    email=models.CharField(max_length=50,default="")
    password=models.CharField(max_length=50,default="")

class Patients(models.Model):
    healthcare=models.CharField(max_length=50,default="")
    name=models.CharField(max_length=50,default="")
    age=models.IntegerField(default="")
    address=models.CharField(max_length=50,default="")
    phone=models.CharField(max_length=50,default="")
    dose=models.IntegerField(default="")
    date_selected=models.CharField(max_length=50,default="")
    
class Vaccine(models.Model):
    name=models.CharField(max_length=50,default="")
    vaccine_id=models.CharField(max_length=50,default="")
    type=models.CharField(max_length=50,default="")
    doses=models.IntegerField(default="")
    start_date=models.DateField(default="")
    end_date=models.DateField(default="")
