from celery import shared_task
from django.conf import settings
from .models import Patient, Doctor, Notification
from twilio.rest import Client  # Make sure 'twilio' is added to your requirements.

@shared_task
def send_notification_task(patient_id, doctor_id, message):
    """
    Send an SMS notification to the patient using Twilio and log the notification.
    """
    try:
        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        if patient.phone_number:
            # Send SMS via Twilio.
            sms = client.messages.create(
                body=message,
                from_=settings.TWILIO_FROM_NUMBER,
                to=patient.phone_number
            )
            status_value = 'SENT'
        else:
            status_value = 'FAILED: No phone number'

    except Exception as e:
        status_value = f'FAILED: {str(e)}'

    # Log the notification.
    Notification.objects.create(
        patient=patient,
        doctor=doctor,
        message=message,
        status=status_value
    )
    return status_value
