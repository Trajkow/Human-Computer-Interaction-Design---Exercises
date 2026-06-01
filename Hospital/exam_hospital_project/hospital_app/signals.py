from .models import Appointment, Patient
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils.timezone import now


@receiver(pre_save, sender=Appointment)
def appointment_status_adjustment(sender, instance, **kwargs):
    if instance.status == 'finished' and instance.datetime > now():
        instance.status = 'scheduled'
    if instance.status == 'scheduled' and instance.datetime < now():
        instance.status = 'finished'

    if instance.pk is None and instance.patient_id is not None:
        doctor = instance.responsible_doctor
        count = Appointment.objects.filter(responsible_doctor=doctor, patient__institution=institution).values("patient_id").distinct().count()
        if count >= 3:
            instance.note = f"High workload with patients from institution {institution}"

@receiver(pre_delete, sender=Patient)
def cleanup_appointments_before_patient_deletion(sender, instance, **kwargs):
    for appt in Appointment.objects.filter(patient=instance):
        if appt.status == 'scheduled':
            appt.delete()
        elif appt.status == 'in_progress':
            appt.note = 'Patient record missing - appointment preserved for audit puposes.'
            appt.save()