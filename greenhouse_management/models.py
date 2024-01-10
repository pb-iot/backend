from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from mapbox_location_field.models import LocationField

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Location(models.Model):
    name = models.CharField(max_length=100)
    coordinates = LocationField()
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name} - {self.coordinates}"

    def __str__(self):
        return f"{self.name} - {self.coordinates}"


class GreenHouse(models.Model):
    class CropTypes(models.TextChoices):
        TOMATOES = "TT", _("Tomatoes")
        POTATOES = "PT", _("Potatoes")

    name = models.CharField(max_length=255)
    crop_type = models.CharField(
        max_length=2,
        choices=CropTypes.choices,
        default=CropTypes.TOMATOES,
    )
    # environment = models.ForeignKey(Environment,
    #                                 on_delete=models.CASCADE) <-- to consider
    #                                 )
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # to consider
    authorized_users = models.ManyToManyField(CustomUser)
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,  # to consider
        related_name="owned_greenhouses",
    )
    # default_environment = models.ForeignKey(Environment,
    # on_delete=models.CASCADE, <-- to consider
    # related_name="default_greenhouses")
    # environments = models.ManyToManyField(Environment, related_name="greenhouses")
    
class Device(models.Model):
    class Functionality(models.TextChoices):
        PASSIVE = "PA", _("Passive device")
        ACTIVE = "AC", _("Active device")

    name = models.CharField(max_length=100)
    functionality = models.CharField(
        max_length=2,
        choices=Functionality.choices,
        default=Functionality.ACTIVE,
        blank=False,
    )
    greenhouse = models.ForeignKey(
        GreenHouse,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
    

class Enviroment(models.Model):
    
    date = models.DateTimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)  
    air_humidity = models.DecimalField(max_digits=5, decimal_places=2)  
    light_level = models.DecimalField(max_digits=5, decimal_places=2)  
    par = models.DecimalField(max_digits=5, decimal_places=2)  
    co2_level = models.DecimalField(max_digits=5, decimal_places=2)  
    soil_moisture_level = models.DecimalField(max_digits=5, decimal_places=2)  
    soil_salinity = models.DecimalField(max_digits=5, decimal_places=2)  
    soil_temperature = models.DecimalField(max_digits=5, decimal_places=2)  
    weight_of_soil_and_plants = models.DecimalField(max_digits=8, decimal_places=2)  
    stem_micro_Variability = models.DecimalField(max_digits=5, decimal_places=2)
