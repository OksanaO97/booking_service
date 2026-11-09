
from django.urls import path
from .views import (BookingServicesListView, home, specialists, bookings, new_booking, detail_view, CommentCreateView, booking_service_form,
                    stock, stock_view, client_profile, statistics, AboutPageView, ContactsPageView, RulesPageView, BarberDetailView,
                    DetailBookingUpdateView, CommentDeleteView)


urlpatterns = [
    path('services/', BookingServicesListView.as_view(), name = 'services'),
    path('home/', home, name = 'homepage'),
    path('specialists/', specialists, name = 'specialists'),
    path('barberdatailview/<int:pk>/', BarberDetailView.as_view(), name = 'barber_detail_view'),
    path('bookings/', bookings, name = 'bookings'),
    path('newbooking/', new_booking, name = 'new_booking'),
    path('bookings/<int:booking_id>/', detail_view, name='booking_detail'),
    path('commentform/', CommentCreateView.as_view(), name='comment_form'),
    path('bookingserviceform/', booking_service_form, name='booking_service_form'),
    path('stockform/', stock, name='stock_form'),
    path('stockview/', stock_view, name='stock_view'),
    path('clientprofile/', client_profile, name='client_profile'),
    path('statistics/', statistics, name='statistics'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('rules/', RulesPageView.as_view(), name='rules'),
    path('bookingupdate/<int:pk>/', DetailBookingUpdateView.as_view(), name='booking_edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

]

