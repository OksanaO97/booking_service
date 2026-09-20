
from django.urls import path
from .views import main_view, schedule_view

urlpatterns = [
    path('brils/', main_view),
    path('schedule/', schedule_view),
]

#/booking_manager/brils/
#/booking_manager/schedule/