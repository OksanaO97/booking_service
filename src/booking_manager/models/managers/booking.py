from django.db import models
from django.utils import timezone


class BookingQuerySet(models.QuerySet):
    def get_upcoming(self):
        return self.filter(
            is_active=True,
            visit_time__gt=timezone.now()
        )




class BookingManager(models.Manager):
    def get_queryset(self):
        return BookingQuerySet(self.model, using=self._db)
    def all_optimize(self):
        return (
        self.get_queryset()
        .prefetch_related(
            'productbooking_set__product'
        )
        .select_related(
            'client__user',
            'barber__user',
            'booking_service'
        )
        )

    def get_upcoming(self):
        return self.get_queryset().get_upcoming()