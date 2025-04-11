from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    # Additional scheduling and availability fields can be added here.

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} ({self.specialization})"

class Patient(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('PENDING', 'PENDING'), ('ONGOING', 'ONGOING'), ('COMPLETED', 'COMPLETED')],
        default='PENDING'
    )

    def __str__(self):
        return f"Appointment: {self.patient.name} with {self.doctor} at {self.scheduled_time}"

class Queue(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    position = models.IntegerField()  # Position in the queue
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Queue pos {self.position} - {self.patient.name} for {self.doctor}"

class Notification(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='PENDING')  # e.g. PENDING, SENT, FAILED

    def __str__(self):
        return f"Notification for {self.patient.name} - Status: {self.status}"
