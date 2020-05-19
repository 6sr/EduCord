from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.views import LogoutView

from main import forms, models

# Create your views here.
def index(request):
    context = {
        "index": True,
    }
    return render(request, 'main/index.html', context)

def institute(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/?next=/institute/')

    context = {
        "institute": True,
    }
    if request.method == 'POST':
        print(request.POST)
        if request.POST['institute_id']:
            # View
            institute_instance = models.Institute.objects.get(id = request.POST['institute_id'])
            context['institute_instance'] = institute_instance
        elif request.POST['institute_instance_id']:
            # Update
            pass
        else:
            # Create
            branch_string = ''
            for i in dict(request.POST)['branch']:
                branch_string += i + ','
            branch_string = branch_string[:-1]
            addressForm = forms.AddressForm(request.POST)
            address = addressForm.save()
            institute_instance = {
                "name": request.POST['name'],
                "branch": branch_string,
                "address": address,
                "phone": request.POST['phone'],
            }
            models.Institute.objects.create(**institute_instance)

    context["institutes"] = models.Institute.objects.all()
    return render(request, 'main/institute.html', context)

# ===================== Student =====================
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    error = None
    if request.method == 'POST':
        loginForm = forms.LoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user:
                # creates session for user in request variable
                auth_login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect('/')
            else:
                error = 'Invalid username or password'
    context = {
        "error": error,
        "login": True,
    }
    return render(request, 'main/login.html', context)

class Logout(LogoutView):
    next_page = '/'

def personalinfo(request):
    context = {
        "student": True,
        "personalinfo": True,
        "student_instance": models.Student.objects.get(roll_no=request.user.get_username())
    }
    return render(request, 'main/student/personalinfo.html', context)

def timetable(request):
    student = models.Student.objects.get(roll_no=request.user.get_username())
    context = {
        "student": True,
        "timetable": True,
        "time_table_instance": {},
    }
    days = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
    for i in range(len(days)):
        day_table = {}
        for j in range(18 - 8):
            start_time = j + 8
            if start_time < 10:
                start_time = '0' + str(start_time)
            try:
                curr = models.TimeTable.objects.get(day = str(i), start_time = str(start_time) + ":00", branch = student.branch).course
            except ObjectDoesNotExist:
                curr = "-"
            day_table[str(start_time)] = curr
        context['time_table_instance'][days[i]] = day_table
    return render(request, 'main/student/timetable.html', context)

def attendance(request):
    context = {
        "student": True,
        "attendance": True,
        "attendance_instance": {},
    }
    if request.method == 'POST':
        student = models.Student.objects.get(roll_no=request.user.get_username())
        from datetime import datetime, timedelta
        date = datetime.strptime(request.POST['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.POST['end_date'], "%Y-%m-%d").date()
        dates = []
        i = 0
        while date <= end_date:
            date_table = {}
            for j in range(18 - 8):
                start_time = j + 8
                if start_time < 10:
                    start_time = '0' + str(start_time)
                try:
                    time_table = models.TimeTable.objects.get(day = date.weekday(), start_time = str(start_time) + ":00", branch = student.branch)
                    curr = models.Attendance.objects.get(date = date, time_table_id = time_table.id, student_id = student.id)
                    curr = 'P' if curr.is_present else 'A'
                except ObjectDoesNotExist:
                    curr = "-"
                date_table[str(start_time)] = curr

            context['attendance_instance'][date] = date_table
            dates.append(date)
            i += 1
            date += timedelta(days=1)

    return render(request, 'main/student/attendance.html', context)

def feepayment(request):
    if request.method == 'POST':
        # Update
        models.FeePaymentStatus.objects.filter(id=request.POST['feepaymentstatus_id']).update(status='p')

    # List
    student = models.Student.objects.get(roll_no=request.user.get_username())
    try:
        feepayments = models.FeePaymentStatus.objects.filter(student_id=student.id)
    except ObjectDoesNotExist:
        feepayments = []

    context = {
        "student": True,
        "feepayment": True,
        "feepayments": feepayments,
    }
    return render(request, 'main/student/feepayment.html', context)

def applicationform(request):
    print("applicationform view 1")
    student = models.Student.objects.get(roll_no=request.user.get_username())
    print("applicationform view 2")

    context = {
        "student": True,
        "applicant": student.id,
        "applicationform": True,
    }
    print("applicationform view 3")
    if request.method == 'POST':
        print("applicationform view 4")
        if request.POST['application_id']:
            # View
            print("applicationform view 5")
            application_instance = models.Application.objects.get(id = request.POST['application_id'])
            print("applicationform view 6")
            context['application_instance'] = application_instance
            print("applicationform view 7")
        else:
            # Create
            print("applicationform view 8")
            application = forms.ApplicationForm(request.POST)
            print("applicationform view 9")
            if application.is_valid():
                print("applicationform view 10")
                application.save()
                print("applicationform view 11")

    print("applicationform view 12")
    context["applicationforms"] = models.Application.objects.filter(applicant_id=student.id)
    print("applicationform view 13")
    return render(request, 'main/student/applicationform.html', context)

