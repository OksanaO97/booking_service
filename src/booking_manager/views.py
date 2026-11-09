from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse, HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils import timezone
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
# CACHE
from django.core.cache import cache
from django.core.cache import caches
from django.conf import settings
from django.db.models import Count, Avg, Sum, Q, F
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import DeleteView






# Главная страница
def home(request):
    template_name = 'booking_manager/home.html'
    return render(request, template_name=template_name)



# Услуги
class BookingServicesListView(ListView):
    model = BookingService
    template_name = 'booking_manager/services.html'
    context_object_name = 'services'

    def get_queryset(self):
        cache_key = 'active_booking_services_list'
        services_list = cache.get(cache_key)
        if services_list is None:
            services_list = list(BookingService.objects.filter(is_active=True))
            cache.set(cache_key, services_list, settings.CACHE_TIMEOUT)
        return services_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        redis_cache = caches['redis']
        redis_key = '5_popular_services_redis'
        popular_services = redis_cache.get(redis_key)

        if popular_services is None:
            average_bookings = BookingService.objects.annotate(this_bookings=Count('bookings')).aggregate(average=Avg('this_bookings'))[
                'average'] or 0
            popular_services = list(BookingService.objects.annotate(all_bookings=Count('bookings')).filter(
                all_bookings__gte=average_bookings, is_active=True).order_by('-all_bookings')[:5])
            redis_cache.set(redis_key, popular_services, timeout=600)

        context['popular_services'] = popular_services
        return context




# Специалисты
def specialists(request):
    template_name = 'booking_manager/specialists.html'
    context = {
        'specialists': Barber.objects.select_related('user').prefetch_related('comments__client__user').all()
    }
    return render(request, template_name=template_name, context=context)




# Страница с детальной информацией о барбере
class BarberDetailView(DetailView):
    template_name = 'booking_manager/barber_detail_view.html'
    model = Barber

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        barber = self.get_object()
        context["comments"] =  Comment.objects.filter(barber=barber).order_by('-created_at')[:5]
        return context




# Удаление комментария
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name_suffix = '_confirm_delete'

    def get_success_url(self):
        barber_id = self.object.barber.id
        return reverse_lazy('barber_detail_view', args=[barber_id])

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Comment.objects.all()

        if hasattr(self.request.user, 'client'):
            current_client = self.request.user.client
            comments = Comment.objects.filter(client=current_client)
            return comments
        return Comment.objects.none()

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        return comment



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
                    form.add_error(None, e)

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
                        product_form.add_error(None, e)
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
                        barber_form.add_error(None, e)

                else:
                    barber_form.add_error(None, "You do not have permission to change the barber for this booking.")
    context = {
        'booking': booking_item,
        'form': product_form,
        'barber_form': barber_form,
    }
    return render(request, template_name=template_name, context=context)




# Редактирование формы бронирвоания
class DetailBookingUpdateView(UpdateView, LoginRequiredMixin):
    model = Booking
    fields = ['visit_time', 'booking_service']
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse_lazy('booking_detail', args=[self.object.id])


    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Booking.objects.all()
        if hasattr(self.request.user, 'client'):
            current_client = self.request.user.client
            bookings = Booking.objects.filter(client=current_client)
            return bookings
        return Booking.objects.none()

    def get_object(self, queryset=None):
        booking = super().get_object(queryset)

        if hasattr(booking, 'is_active') and not booking.is_active:
            raise PermissionDenied("You cannot edit inactive bookings.")
        return booking




# Форма для комментариев
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'booking_manager/comment_form.html'
    success_url = reverse_lazy("specialists")

    def form_valid(self, form):
        if hasattr(self.request.user, 'client'):
            current_barber = form.cleaned_data["barber"]
            current_client = self.request.user.client
            current_booking = Booking.objects.filter(client=current_client, barber=current_barber).last()

            form.instance.client = current_client
            form.instance.booking = current_booking

            return super().form_valid(form)
        else:
            form.add_error(None, "You do not have a client profile. You cannot leave a review for a specialist.")
            return self.form_invalid(form)




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




# Отдельная страница для клиента с информацией по бронированиям, профиль клиента
@login_required
def client_profile(request):
    if not (request.user.is_staff or hasattr(request.user, 'client')):
        return HttpResponseRedirect(reverse('homepage'))

    template_name = 'booking_manager/client_profile.html'
    cache_key = ('active_client_profile_list' + str(request.user.id))
    profile = cache.get(cache_key)
    if hasattr(request.user, 'client'):
        status = getattr(request.user.client, 'status', 'Active')
        bookings_count = request.user.client.bookings.count()
    else:
        bookings_count = 0
        status = 'Administrator'

    if profile is None:
        profile = {'client_name': request.user.first_name,
                   'status':status,
                   'bookings':bookings_count}
        cache.set(cache_key, profile, 900)
    context = {
        'profile':profile
        }
    return render(request, template_name=template_name, context=context)



# Для персонала: перемещение остатков товара между барбершопами
@login_required
def stock(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('homepage'))
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
                form.add_error(None, e)

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



# Статистика для персонала
@login_required
def statistics(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('homepage'))
    template_name = 'booking_manager/statistics.html'
    cache_key = 'statistics_list'
    stat = cache.get(cache_key)
    start_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0)

    if stat is None:
        bookings = Booking.objects.filter(created_at__gte=start_of_month).count()
        revenue = BookingService.objects.aggregate(total_revenue=Sum(F('price'), filter=Q(bookings__created_at__gte=start_of_month)))['total_revenue'] or 0
        rating_data = Barber.objects.filter(bookings__created_at__gte=start_of_month).aggregate(rat=Avg('rating'))['rat']
        rating = round(rating_data or 0, 2)
        stat = {"bookings": bookings,
                'revenue': revenue,
                'rating': rating}
        cache.set(cache_key, stat, 600)

    context = {
        'stat': stat
    }
    return render(request, template_name=template_name, context=context)


# Страница "О нас"
class AboutPageView(TemplateView):
    template_name = "booking_manager/about.html"


# Страница контактов
class ContactsPageView(TemplateView):
    template_name = "booking_manager/contacts.html"


# Правила посещения барбершопа
class RulesPageView(TemplateView):
    template_name = "booking_manager/rules.html"
























# @login_required
# def comment_form(request):
#     template_name = 'booking_manager/comment_form.html'
#
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             if hasattr(request.user, 'client'):
#                 current_barber = form.cleaned_data["barber"]
#                 rating_value = form.cleaned_data["rating"]
#                 text_value = form.cleaned_data["text"]
#                 current_client = request.user.client
#                 current_booking = Booking.objects.filter(client=current_client, barber=current_barber).last()
#
#                 Comment.objects.create(
#                     client=current_client,
#                     barber=current_barber,
#                     rating=rating_value,
#                     text=text_value,
#                     booking=current_booking,
#                 )
#
#                 return HttpResponseRedirect(reverse("specialists"))
#             else:
#                 form.add_error(None, "You do not have a client profile. You cannot leave a review for a specialist.")
#
#     else:
#         form = CommentForm()
#
#     context = {"form": form}
#     return render(request, template_name=template_name, context=context)






# Тестовая вьюшка для дженериков
# class MyView(View):
#     def get(self, request, *args, **kwargs):
#         return HttpResponse('<h1>GET Hello</h1>')
#
#     def post(self, request, *args, **kwargs):
#         return HttpResponse('<h1>POST Hello</h1>')


# class AboutPageView(TemplateView):
#     template_name = "about.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["latest_articles"] = Article.objects.all()[:5]
#         return context





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



# @login_required
# def client_profile(request):
#     if not hasattr(request.user, 'client'):
#         return HttpResponseRedirect(reverse('homepage'))
#     template_name = 'booking_manager/client_profile.html'
#     cache_key = ('active_client_profile_list' + str(request.user.client.id))
#     profile = cache.get(cache_key)
#     bookings_count = request.user.client.bookings.count()
#
#     if profile is None:
#         profile = {'client_name': request.user.first_name,
#                    'status':request.user.client.status,
#                    'bookings':bookings_count}
#         cache.set(cache_key, profile, 900)
#     context = {
#         'client': request.user.client,
#         'bookings':  bookings_count,
#         'profile':profile
#         }
#     return render(request, template_name=template_name, context=context)

 # average_bookings = BookingService.objects.annotate(this_bookings=Count('bookings')).aggregate(average=Avg('this_bookings'))['average'] or 0
 #    popular_services = BookingService.objects.annotate(all_bookings=Count('bookings')).filter(all_bookings__gte=average_bookings, is_active=True).order_by('-all_bookings')
 #    context = {'services': services,
 #               'popular_services': popular_services}


# @cache_page(settings.CACHE_TIMEOUT, key_prefix="booking1")