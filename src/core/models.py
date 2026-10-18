from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True



class RatingMixin(models.Model):
    rating = models.FloatField(
        verbose_name='оценка',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True