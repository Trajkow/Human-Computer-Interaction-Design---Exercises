from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import AppointmentForm
from hospital_app.models import Doctor, Appointment, AppointmentAssignment


# Create your views here.
def index(request):
    cardiologists = Doctor.objects.filter(speciality='cardiologist')
    dermatologist = Doctor.objects.filter(speciality='dermatologist')
    neurologist = Doctor.objects.filter(speciality='neurologist')

    return render(request, "index.html", {
        "cardiologists": cardiologists,
        "dermatologists": dermatologist,
        "neurologists": neurologist
    })

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.responsible_doctor = doctor
            appt.appointment_type = doctor.speciality
            appt.save()
            AppointmentAssignment.objects.create(appointment=appt, doctor=doctor)
            return redirect("doctor_detail", doctor_id=doctor.id)
    else:
        form = AppointmentForm()

    now = timezone.now()
    appts = Appointment.objects.filter(responsible_doctor=doctor)

    return render(request, "doctor_detail.html", {
        "doctor": doctor,
        "form": form,
        "past_appointments": appts.filter(datetime__lt=now, status="finished"),
        "today_appointments": appts.filter(datetime__date=now.date()),
        "future_appointments": appts.filter(datetime__gt=now, status="scheduled"),
    })