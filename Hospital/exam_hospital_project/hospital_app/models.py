from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Doctor(models.Model):

    speciality_choices = [
        ('cardiologist', 'Cardiologist'),
        ('dermatologist', 'Dermatologist'),
        ('neurologist', 'Neurologist')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    speciality = models.CharField(max_length=100, null=True, blank=True, choices=speciality_choices)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    institution = models.CharField(max_length=100, null=True, blank=True)
    num_completed_appointments = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.last_name} - {self.speciality}'

class Patient(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.last_name}'


class Appointment(models.Model):

    appointment_type_choices = [
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('neurology', 'Neurology'),
    ]

    status_choices = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]

    type = models.CharField(max_length=100, null=True, blank=True, choices=appointment_type_choices)
    symptom_description = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True, choices=status_choices)
    datetime = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    patient = (models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True))
    responsible_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='responsible_appointments')

    def __str__(self):
        return f'{self.type} {self.symptom_description} - {self.status}'

class AppointmentAssignment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('appointment', 'doctor')

    def __str__(self):
        return f'{self.appointment} - {self.doctor}'