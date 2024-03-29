from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import *
from datetime import datetime


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="foo"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )

            filter(catergory=map(lambda key: "europe" in key))


class LocationTestCase(TestCase):
    def create_location(self, owner, name="Bialystok", point=None):
        return Location.objects.create(name=name, coordinates=point, owner=owner)

    def test_create_location_creation(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal3@user.com", password="foo")
        coords = (42.12345, -71.98765)
        created_obj = self.create_location(user, point=coords)
        created_obj.save()
        filtered_obj = Location.objects.get(id=created_obj.id)

        self.assertTrue(isinstance(filtered_obj, Location))
        self.assertTrue(Location.objects.filter(coordinates=coords).exists())


class GreenHouseTestCase(TestCase):
    def test_greenhouse_creation(self):
        name = "TomatoTomato"
        crop_type = "TT"
        User = get_user_model()
        owner = User.objects.create_user(email="owner@user.com", password="foo")
        user_1 = User.objects.create_user(email="normal1@user.com", password="foo")
        user_2 = User.objects.create_user(email="normal2@user.com", password="foo")
        authorized_users = [user_1, user_2]
        location = Location.objects.create(name="Bialystok", coordinates=(42.12345, -71.98765), owner=user_1)
        # environment <-- add test
        # devices <-- add test
        # default_environment <-- add test
        # environments <-- add test

        obj = GreenHouse.objects.create(name=name, location=location, owner=owner)
        obj.authorized_users.set(authorized_users)

        self.assertTrue(isinstance(obj, GreenHouse))
        self.assertTrue(
            GreenHouse.objects.filter(
                name=name,
                crop_type=crop_type,
                location=location,
                authorized_users__in=[user_1.id, user_2.id],
                owner=owner,
            ).exists()
        )

    def test_crop_type_choices(self):
        # Test if crop_types contains one of available options

        # Case 1: option: 'Tomatoes' (TOMATOES)
        greenhouse_tomatoes = GreenHouse(crop_type=GreenHouse.CropTypes.TOMATOES)
        self.assertEqual(greenhouse_tomatoes.crop_type, "TT")

        # Case 2: option: 'Potatoes' (POTATOES)
        greenhouse_potatoes = GreenHouse(crop_type=GreenHouse.CropTypes.POTATOES)
        self.assertEqual(greenhouse_potatoes.crop_type, "PT")

        # Case 3: option: default should be 'Tomatoes'
        default_greenhouse = GreenHouse()
        self.assertEqual(default_greenhouse.crop_type, "TT")


class DeviceTestCase(TestCase):
    def device_creation(self):
        User = get_user_model()
        owner = User.objects.create_user(email="owner@user.com", password="foo")
        location = Location.objects.create(name="Bialystok", coordinates=(42.12345, -71.98765), owner=owner)
        greenhouse = GreenHouse.objects.create(name="TestGreenHouse", location=location, owner=owner)
        return Device.objects.create(name="Fan", functionality="AC", greenhouse=greenhouse)

    def test_device_creation(self):
        device = self.device_creation()
        self.assertEqual(device.name, "Fan")
        functionality_choices = dict(device.Functionality.choices)
        self.assertIn(device.functionality, functionality_choices)
        self.assertTrue(isinstance(device, Device))
        self.assertTrue(Device.objects.filter(name="Fan").exists())


class EnvironmentTestCase(TestCase):
    def create_environment(self, date=datetime(2023, 10, 17),
                           temperature=12.0,
                           air_humidity=60.0,
                           light_level=100.0,
                           par=400.0,
                           co2_level=500.0,
                           soil_moisture_level=40.0,
                           soil_salinity=1.5,
                           soil_temperature=20.0,
                           weight_of_soil_and_plants=1000,
                           stem_micro_variability=0.2):
        User = get_user_model()
        owner = User.objects.create_user(email="owner@user.com", password="foo")
        location = Location.objects.create(name="Bialystok", coordinates=(42.12345, -71.98765), owner=owner)
        green_house = GreenHouse.objects.create(name="Green house", location=location, owner=owner)

        return Environment.objects.create(
            green_house=green_house,
            date=date,
            temperature=temperature,
            air_humidity=air_humidity,
            light_level=light_level,
            par=par,
            co2_level=co2_level,
            soil_moisture_level=soil_moisture_level,
            soil_salinity=soil_salinity,
            soil_temperature=soil_temperature,
            weight_of_soil_and_plants=weight_of_soil_and_plants,
            stem_micro_variability=stem_micro_variability)

    def test_environment_creation(self):
        obj = self.create_environment()
        self.assertTrue(isinstance(obj, Environment))
        self.assertTrue(Environment.objects.get(id=obj.id))
