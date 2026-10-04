from django.shortcuts import render, HttpResponse

def home(request):
    template_name = 'booking_manager/home.html'
    return render(request, template_name=template_name)


def services(request):
    template_name = 'booking_manager/services.html'
    services_list = [
    {"id": 1, "name": "Haircut", "duration": 60, "price": 30, "category": "Hair"},
    {"id": 2, "name": "Beard Trim", "duration": 30, "price": 15, "category": "Hair"},
    {"id": 3, "name": "Manicure", "duration": 45, "price": 25, "category": "Nails"},
    {"id": 4, "name": "Massage", "duration": 90, "price": 50, "category": "Wellness"},
    {"id": 5, "name": "Consultation", "duration": 30, "price": 20, "category": "Other"}
    ]
    context = {'services': services_list}
    return render(request, template_name=template_name, context=context)


def specialists(request):
    template_name = 'booking_manager/specialists.html'
    specialists_list = [
    {"id": 1, "name": "Alice Brown", "speciality": "Hair Stylist", "experience": 5},
    {"id": 2, "name": "Bob Smith", "speciality": "Barber", "experience": 7},
    {"id": 3, "name": "Diana Green", "speciality": "Nail Artist", "experience": 3},
    {"id": 4, "name": "Charlie White", "speciality": "Massage Therapist", "experience": 6}
    ]
    context = {'specialists': specialists_list}
    return render(request, template_name=template_name, context=context)


def bookings(request):
    template_name = 'booking_manager/bookings.html'
    bookings_list = [
    {"client": "John", "service": "Haircut", "date": "20.09.2026", "time": "12:00", "status": "confirmed"},
    {"client": "Anna", "service": "Manicure", "date": "20.09.2026", "time": "14:30", "status": "pending"},
    {"client": "Mike", "service": "Massage", "date": "21.09.2026", "time": "10:00", "status": "confirmed"},
    {"client": "Kate", "service": "Consultation", "date": "22.09.2026", "time": "16:00", "status": "cancelled"}
    ]
    context = {'bookings': bookings_list}
    return render(request, template_name=template_name, context=context)


def new_booking(request):
    template_name = 'booking_manager/new_booking.html'
    return render(request, template_name=template_name)
