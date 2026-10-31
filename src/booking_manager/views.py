from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from booking_manager.models import Booking, BookingService, Comment
from account.models import Barber, Client
from booking_manager.forms import CommentForm, BookingForm, BookingServiceForm, ProductBookingForm



def home(request):
    template_name = 'booking_manager/home.html'
    return render(request, template_name=template_name)


def services(request):
    template_name = 'booking_manager/services.html'
    context = {'services': BookingService.objects.all()}
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

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user.client
            booking.save()


            return HttpResponseRedirect(reverse("bookings"))

    else:
        form = BookingForm()
    context = {"form": form}

    return render(request, template_name=template_name, context=context)



def detail_view(request, booking_id):
    template_name = 'booking_manager/detail_view.html'
    booking_item = get_object_or_404(Booking.objects.all_optimize(),id=booking_id)
    if request.method == "POST":
        form = ProductBookingForm(request.POST)
        if form.is_valid():

            pb = form.save(commit=False)
            pb.booking = booking_item
            pb.total_price = pb.quantity * pb.product.price
            pb.save()


            return HttpResponseRedirect(reverse("booking_detail", args=[booking_id]))

    else:
        form = ProductBookingForm()
    context = {
        'booking': booking_item,
        "form": form,
    }

    return render(request, template_name=template_name, context=context)



def comment_form(request):
    template_name = 'booking_manager/comment_form.html'

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            current_barber = form.cleaned_data["barber"]
            rating_value = form.cleaned_data["rating"]
            text_value = form.cleaned_data["text"]
            current_client = request.user.client
            current_booking = Booking.objects.filter(client=current_client, barber=current_barber).last()

            Comment.objects.create(
                client=current_client,
                barber=current_barber,
                rating=rating_value,
                text=text_value,
                booking=current_booking,
            )

            return HttpResponseRedirect(reverse("specialists"))

    else:
        form = CommentForm()

    context = {"form": form}
    return render(request, template_name=template_name, context=context)



def booking_service_form(request):
    template_name = 'booking_manager/booking_service_form.html'

    if request.method == "POST":
        form = BookingServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("services"))

    else:
        form = BookingServiceForm()

    context = {"form": form}
    return render(request, template_name=template_name, context=context)









# def book_form(request):
#     template_name = 'booking_manager/booking_form.html'
#
    # if request.method == "POST":
    #     form = BookingForm(request.POST)
    #     if form.is_valid():
    #         Booking.objects.create(**form.cleaned_data)
    #         return HttpResponseRedirect(reverse("bookings"))
    #
    # else:
    #     form = BookingForm()
    # context = {"form": form}
    #
    # return render(request, template_name=template_name, context=context)




# def book_form(request):
#     template_name = 'booking_manager/booking_form.html'
#
#     if request.method == "POST":
#         form = BookingForm(request.POST)
#         if form.is_valid():
#
#             booking = form.save(commit=False)
#             booking.client = getattr(
#                 request.user, "client", Client.objects.first()
#             )
#             booking.barber = Barber.objects.first()
#             booking.booking_service = BookingService.objects.first()
#             booking.save()
#
#             return HttpResponseRedirect(reverse("bookings"))
#
#     else:
#         form = BookingForm()
#     context = {"form": form}
#
#     return render(request, template_name=template_name, context=context)
