from django.shortcuts import render, get_object_or_404
from booking_manager.models import Booking
from account.models import Barber

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
    context = {
        'specialists': Barber.objects.select_related('user').prefetch_related('comments__client__user').all()
    }
    return render(request, template_name=template_name, context=context)


def bookings(request):
    template_name = 'booking_manager/bookings.html'
    context = {
        "bookings": Booking.objects.all_optimize().get_upcoming()
    }
    return render(request, template_name=template_name, context=context)


def new_booking(request):
    template_name = 'booking_manager/new_booking.html'
    return render(request, template_name=template_name)


def detail_view(request, booking_id):
    template_name = 'booking_manager/detail_view.html'
    booking_item = get_object_or_404(Booking.objects.all_optimize(),id=booking_id)
    context = {
        'booking': booking_item
    }
    return render(request, template_name=template_name, context=context)



