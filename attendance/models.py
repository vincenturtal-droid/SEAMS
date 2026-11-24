import qrcode
import uuid
from io import BytesIO
from django.core.files import File
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    student_number = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    year_level = models.CharField(max_length=20)
    section = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_number})"

class Event(models.Model):
    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    event_name = models.CharField(max_length=150)
    description = models.TextField()
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    venue = models.CharField(max_length=150)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Upcoming')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_name

class QrCode(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='qr_code_obj')
    qr_token = models.CharField(max_length=255, unique=True, blank=True)
    qr_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.qr_token:
            self.qr_token = str(uuid.uuid4())
            
            # Generate QR Image
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.qr_token)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            file_name = f'qr_{self.qr_token}.png'
            self.qr_image.save(file_name, File(buffer), save=False)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"QR for {self.event.event_name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendance_time = models.DateTimeField(auto_now_add=True)
    attendance_method = models.CharField(max_length=20, default='QR Code') # QR Code or Manual
    status = models.CharField(max_length=20, default='Present')

    class Meta:
        unique_together = ('student', 'event') # Nagpugong sa duplicate attendance

    def __str__(self):
        return f"{self.student} - {self.event} ({self.status})"