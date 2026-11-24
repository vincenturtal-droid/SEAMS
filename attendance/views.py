from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Event, QrCode, Attendance
from .forms import StudentForm

def dashboard_view(request):
    total_students = Student.objects.count()
    total_events = Event.objects.count()
    total_attendance = Attendance.objects.count()
    recent_attendance = Attendance.objects.all().order_by('-attendance_time')[:5]
    
    context = {
        'total_students': total_students,
        'total_events': total_events,
        'total_attendance': total_attendance,
        'recent_attendance': recent_attendance,
    }
    return render(request, 'attendance/dashboard.html', context)

def student_list_view(request):
    students = Student.objects.all()
    return render(request, 'attendance/students.html', {'students': students})

def add_student_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'attendance/add_student.html', {'form': form})

def event_list_view(request):
    events = Event.objects.all()
    return render(request, 'attendance/events.html', {'events': events})

def scanner_view(request):
    return render(request, 'attendance/scanner.html')