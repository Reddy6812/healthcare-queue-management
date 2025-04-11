from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Max
from django.contrib.auth.models import User

from .models import Patient, Doctor, Appointment, Queue
from .serializers import PatientSerializer, DoctorSerializer, AppointmentSerializer, QueueSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# ViewSets for Patients, Doctors, and Appointments.
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enqueue_patient(request):
    """
    Add a patient to a doctor's queue.
    Expects JSON with "doctor_id" and "patient_id".
    """
    doctor_id = request.data.get('doctor_id')
    patient_id = request.data.get('patient_id')
    if not doctor_id or not patient_id:
        return Response({'error': 'Missing doctor_id or patient_id.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        doctor = Doctor.objects.get(id=doctor_id)
        patient = Patient.objects.get(id=patient_id)
    except (Doctor.DoesNotExist, Patient.DoesNotExist):
        return Response({'error': 'Invalid doctor or patient ID.'}, status=status.HTTP_404_NOT_FOUND)

    max_position = Queue.objects.filter(doctor=doctor).aggregate(Max('position'))['position__max']
    new_position = (max_position or 0) + 1

    queue_entry = Queue.objects.create(doctor=doctor, patient=patient, position=new_position)
    return Response(QueueSerializer(queue_entry).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_queue(request, doctor_id):
    """
    Return the queue for the specified doctor.
    """
    queue_entries = Queue.objects.filter(doctor__id=doctor_id).order_by('position')
    serializer = QueueSerializer(queue_entries, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])  # Only staff/admin users can trigger notify_next.
def notify_next_in_queue(request):
    """
    Remove the first patient from the queue, recalculate positions,
    send notification (using Celery task), and push a real‑time update.
    Expects JSON with "doctor_id".
    """
    doctor_id = request.data.get('doctor_id')
    if not doctor_id:
        return Response({'error': 'Missing doctor_id.'}, status=status.HTTP_400_BAD_REQUEST)

    queue_entries = Queue.objects.filter(doctor__id=doctor_id).order_by('position')
    if not queue_entries.exists():
        return Response({'message': 'Queue is empty.'})

    # Remove the patient at the head of the queue.
    first = queue_entries.first()
    first.delete()

    # Recalculate positions.
    new_queue_entries = Queue.objects.filter(doctor__id=doctor_id).order_by('position')
    for idx, entry in enumerate(new_queue_entries):
        entry.position = idx + 1
        entry.save()

    # Trigger notification via Celery (see tasks.py).
    from .tasks import send_notification_task
    if new_queue_entries.exists():
        next_patient = new_queue_entries.first().patient
        message = "It is your turn. Please proceed to the doctor's office."
        send_notification_task.delay(next_patient.id, doctor_id, message)

    # Send updated queue over WebSocket to all subscribed clients.
    channel_layer = get_channel_layer()
    queue_data = QueueSerializer(new_queue_entries, many=True).data
    async_to_sync(channel_layer.group_send)(
        f'queue_{doctor_id}',
        {
            "type": "send_queue_update",
            "message": f"Updated Queue: {queue_data}"
        }
    )

    return Response({'message': 'Queue updated and next patient notified.'})
