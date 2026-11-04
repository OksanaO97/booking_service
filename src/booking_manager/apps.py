from django.apps import AppConfig



class BookingManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booking_manager'
    verbose_name = 'Менеджер бронирований'
    verbose_name_plural = 'Менеджер бронирований'



    def ready(self):
        # from booking_manager.signals.bookings_products_signal import signal_post_save_booking_with_service_1
        # post_save.connect(signal_post_save_booking_with_service_1)

        from booking_manager.signals import barbers_comments_signal
        from booking_manager.signals import bookings_products_signal
        from booking_manager.signals import users_clients_signal
        from booking_manager.signals import clients_booking_signal

