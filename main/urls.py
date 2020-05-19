from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('institute/', views.institute, name = 'institute'),

    path('login/', views.login, name = 'login'),
    path('logout/', views.Logout.as_view(), name = 'logout'),

    path('student/personalinfo/', views.personalinfo, name = 'personalinfo'),
    path('student/timetable/', views.timetable, name = 'timetable'),
    path('student/attendance/', views.attendance, name = 'attendance'),
    path('student/feepayment/', views.feepayment, name = 'feepayment'),
    path('student/applicationform/', views.applicationform, name = 'applicationform'),
]

