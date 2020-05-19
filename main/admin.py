from django.contrib import admin

from main import models
# Register your models here.
admin.site.register([
    models.Address,
    models.Student_Address,
    models.Institute,
    models.Student,
    models.TimeTable,
    models.Attendance,
    models.FeePayment,
    models.FeePaymentStatus,
    models.Application,
    models.Subscribe,
])
