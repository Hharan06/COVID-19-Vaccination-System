from django.contrib import admin
from .models import HealthCareInformation,Login,Patients,Vaccine

# Register your models here.
admin.site.register(HealthCareInformation)
admin.site.register(Login)
admin.site.register(Patients)
admin.site.register(Vaccine)