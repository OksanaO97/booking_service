from django.db import models

class ProductQuerySet(models.QuerySet):

    def annotate_product_count(self):
        return (self.filter()
        .annotate(
            count_book=models.Count('bookings'))
        .filter(
            count_book__gte=2,
            price__gte=models.Avg('price'))
        )



class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def annotate_product_count(self):
        return self.get_queryset().annotate_product_count()



