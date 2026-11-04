from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
# модели
from booking_manager.models import Booking, BookingService, Comment, ProductStock
from account.models import Barber
# формы
from booking_manager.forms import CommentForm, BookingForm, BookingServiceForm, ProductBookingForm, BarberForm, StockForm
# транзакции
from booking_manager.transactions.product_booking_transaction import create_product_booking_transaction
from booking_manager.transactions.barber_transaction import change_barbers_transaction
from booking_manager.transactions.book_barber_transaction import create_booking_transaction
from booking_manager.transactions.barbershop_product_transaction import move_product_transaction



# Главная страница
def home(request):
    template_name = 'booking_manager/home.html'
    return render(request, template_name=template_name)



# Услуги
def services(request):
    template_name = 'booking_manager/services.html'
    context = {'services': BookingService.objects.all()}
    return render(request, template_name=template_name, context=context)



# Специалисты
def specialists(request):
    template_name = 'booking_manager/specialists.html'
    context = {
        'specialists': Barber.objects.select_related('user').prefetch_related('comments__client__user').all()
    }
    return render(request, template_name=template_name, context=context)



# Бронирования
def bookings(request):
    template_name = 'booking_manager/bookings.html'
    context = {
        "bookings": Booking.objects.all_optimize().get_upcoming()
    }
    return render(request, template_name=template_name, context=context)



# Создание нового бронирования
@login_required
def new_booking(request):
    template_name = 'booking_manager/new_booking.html'
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():

            if hasattr(request.user, 'client'):
                booking = form.save(commit=False)
                booking.client = request.user.client

                try:
                    create_booking_transaction(
                        booking=booking,
                        barber=form.cleaned_data['barber'],
                    )

                    return HttpResponseRedirect(reverse("bookings"))
                except ValidationError as e:
                    form.add_error('barber', e.message)

            else:
                form.add_error(None, 'You do not have a client profile. You cannot book a specialist.')


    else:
        form = BookingForm()
    context = {"form": form}

    return render(request, template_name=template_name, context=context)


# Подробности бронирования, добавление товаров, смена барбера
@login_required
def detail_view(request, booking_id):
    template_name = 'booking_manager/detail_view.html'
    booking_item = get_object_or_404(Booking.objects.all_optimize(),id=booking_id)

    product_form = ProductBookingForm()
    barber_form = BarberForm(initial={'barber': booking_item.barber})

    # Отрабатывает форма для добавления товаров
    if request.method == "POST":
        if "add_product" in request.POST:
            product_form = ProductBookingForm(request.POST)
            if product_form.is_valid():
                if request.user.is_staff or booking_item.client == getattr(request.user, 'client', None):

                    try:
                        create_product_booking_transaction(
                            booking_item= booking_item,
                            product=product_form.cleaned_data['product'],
                            quantity=product_form.cleaned_data['quantity']
                        )

                        return HttpResponseRedirect(reverse("booking_detail", args=[booking_id]))
                    except ValidationError as e:
                        product_form.add_error('quantity', e.message)
                else:
                    product_form.add_error(None, "You do not have permission to modify this booking.")


        # Отрабатывает форма для смены барбера
        elif "change_barber" in request.POST:
            barber_form = BarberForm(request.POST)
            if barber_form.is_valid():
                if request.user.is_staff or booking_item.client == getattr(request.user, 'client', None):

                    try:
                        change_barbers_transaction(
                            booking_item=booking_item,
                            new_barber=barber_form.cleaned_data['barber']
                        )
                        return HttpResponseRedirect(reverse("booking_detail", args=[booking_id]))
                    except ValidationError as e:
                        barber_form.add_error('barber', e.message)

                else:
                    barber_form.add_error(None, "You do not have permission to change the barber for this booking.")
    context = {
        'booking': booking_item,
        'form': product_form,
        'barber_form': barber_form,
    }
    return render(request, template_name=template_name, context=context)



# Форма для комментариев
@login_required
def comment_form(request):
    template_name = 'booking_manager/comment_form.html'

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            if hasattr(request.user, 'client'):
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
                form.add_error(None, "You do not have a client profile. You cannot leave a review for a specialist.")

    else:
        form = CommentForm()

    context = {"form": form}
    return render(request, template_name=template_name, context=context)



# Для персонала: добавление услуги
@login_required
def booking_service_form(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('home'))
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



# Для персонала: перемещение остатков товара между барбершопами
@login_required
def stock(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('home'))
    template_name = 'booking_manager/stock.html'
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            try:
                move_product_transaction(
                    product_id = form.cleaned_data['product_id'],
                    barbershop_from=form.cleaned_data['barbershop_from'],
                    barbershop_to=form.cleaned_data['barbershop_to'],
                    quantity=form.cleaned_data['quantity']
                )

                return HttpResponseRedirect(reverse("stock_view"))
            except ValidationError as e:
                form.add_error('quantity', e.message)

    else:
        form = StockForm()

    context = {"form": form}
    return render(request, template_name=template_name, context=context)



# Для персонала: список всех остатков
@login_required
def stock_view(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('home'))

    template_name = 'booking_manager/stock_view.html'
    product_stock_queryset = ProductStock.objects.select_related('product', 'barbershop').all()
    context = {
        "productstock": product_stock_queryset
    }
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



# def bookings(request):
#     template_name = 'booking_manager/bookings.html'
#     with transaction.atomic():
#         Booking.objects.filter(id__gte=560, id__lte=566).select_for_update()
#     for i in range(60):
#         print(i)
#         time.sleep(1)
#
#         raise
#     raise
#     context = {
#         "bookings": Booking.objects.all_optimize().get_upcoming()
#     }
#     return render(request, template_name=template_name, context=context)