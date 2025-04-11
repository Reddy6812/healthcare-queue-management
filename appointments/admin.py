from django.contrib import admin
from .models import Doctor, Patient, Appointment, Queue, Notification

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Queue)
admin.site.register(Notification)
