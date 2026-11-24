from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('students/', views.student_list_view, name='student_list'),
    path('students/add/', views.add_student_view, name='add_student'),
    path('events/', views.event_list_view, name='event_list'),
    path('scanner/', views.scanner_view, name='scanner'),
]