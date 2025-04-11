from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DoctorViewSet, AppointmentViewSet, enqueue_patient, get_queue, notify_next_in_queue

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('enqueue/', enqueue_patient, name='enqueue'),
    path('queue/<int:doctor_id>/', get_queue, name='get_queue'),
    path('notify-next/', notify_next_in_queue, name='notify_next'),
]
