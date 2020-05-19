from django.db import models

# Create your models here.
class Address(models.Model):
    line1 = models.CharField(max_length=256)
    line2 = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    pincode = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = "Address"

class Institute(models.Model):
    name = models.CharField(max_length=256)
    branch = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    phone = models.CharField(max_length=256)

    def get_branch_list(self):
        return self.branch.split(',')

    def __str__(self):
        return self.name

class Student(models.Model):
    GENDER = (
        ('m', 'Male'),
        ('f', 'Female')
    )
    roll_no = models.CharField(max_length = 256)
    dob = models.DateField()
    gender = models.CharField(max_length = 1, choices = GENDER)
    branch = models.CharField(max_length=256)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

    father_name = models.CharField(max_length=256)
    father_phone = models.CharField(max_length=256)
    father_email = models.EmailField()

    mother_name = models.CharField(max_length=256)
    mother_phone = models.CharField(max_length=256)
    mother_email = models.EmailField()

    annual_income = models.CharField(max_length=20)
    has_institute_access = models.BooleanField(default=False)

    image = models.CharField(max_length=256, default = '/static/img/default-user-image.png')
    def __str__(self):
        return self.roll_no

class Student_Address(models.Model):
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Student Address"

class TimeTable(models.Model):
    DAY_NAMES = (
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    )
    # 05:00
    start_time = models.CharField(max_length=5)
    day = models.CharField(max_length = 1, choices = DAY_NAMES)
    # In Minutes
    duration = models.CharField(max_length=5, default = '60')
    course = models.CharField(max_length=20)
    branch = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Time Table"

class Attendance(models.Model):
    time_table = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    date = models.DateField()

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Attendance"


class FeePayment(models.Model):
    branch = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    amount = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name_plural = "Fee Payment"

class FeePaymentStatus(models.Model):
    PAYMENT_STATUS = (
        ('p', 'Paid'),
        ('u', 'Unpaid'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fees = models.ForeignKey(FeePayment, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=PAYMENT_STATUS)

    class Meta:
        verbose_name_plural = "Fee Payment Status"

class Application(models.Model):
    applicant = models.ForeignKey(Student, on_delete=models.CASCADE)
    department = models.CharField(max_length=256)
    subject = models.CharField(max_length=256)
    status = models.CharField(max_length=256)
    applied_on = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=256)

class Subscribe(models.Model):
    email = models.EmailField()

