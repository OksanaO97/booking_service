from django.db import models

class CategoryChoices(models.TextChoices):
    MASSAGE = "massage"
    MOUSTACHE = "moustache"
    BEARD = "beard"
    HAIRCUT = "haircut"
