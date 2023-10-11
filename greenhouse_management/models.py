from django.db import models


class Localization(models.Model):
    name = models.CharField(max_length=100)

