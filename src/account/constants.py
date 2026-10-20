from django.db import models

class ClientStatusChoices(models.TextChoices):
    NOOB = "noob"
    BEGINNER = "beginner"
    EXPERT = "expert"
    LEGEND = "legend"
