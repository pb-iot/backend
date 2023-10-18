from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Localization, GreenHouse, Enviroment
from datetime import datetime

class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
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
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
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
                email='super@user.com', password='foo', is_superuser=False)

            filter(catergory=map(lambda key: 'europe' in key))


class LocalizationTestCase(TestCase):

    def create_localization(self, name="Bialystok"):
        return Localization.objects.create(name=name)

    def test_localization_creation(self):
        obj = self.create_localization()
        self.assertTrue(isinstance(obj, Localization))
        self.assertTrue(Localization.objects.filter(name="Bialystok").exists())


class GreenHouseTestCase(TestCase):
        
    def test_greenhouse_creation(self):
        name = "TomatoTomato"
        crop_type = 'TT'
        User = get_user_model()
        owner =  User.objects.create_user(
            email='owner@user.com', password='foo')
        user_1 =  User.objects.create_user(
            email='normal1@user.com', password='foo')
        user_2 =  User.objects.create_user(
            email='normal2@user.com', password='foo')
        authorized_users = [user_1, user_2]
        location = Localization.objects.create(name= "Bialystok")
        # environment <-- add test
        # devices <-- add test
        # default_environment <-- add test
        # environments <-- add test

        obj = GreenHouse.objects.create(name= name,
                                        location= location,
                                        owner= owner)
        obj.authorized_users.set(authorized_users)
        
        self.assertTrue(isinstance(obj, GreenHouse))
        self.assertTrue(GreenHouse.objects.filter(name= name, 
                                                  crop_type= crop_type,
                                                  location= location,
                                                  authorized_users__in= [user_1.id, user_2.id],
                                                  owner= owner).exists())


    def test_crop_type_choices(self):
        # Test if crop_types contains one of available options
        
        # Case 1: option: 'Tomatoes' (TOMATOES)
        greenhouse_tomatoes = GreenHouse(crop_type=GreenHouse.CropTypes.TOMATOES)
        self.assertEqual(greenhouse_tomatoes.crop_type, 'TT')

        # Case 2: option: 'Potatoes' (POTATOES)
        greenhouse_potatoes = GreenHouse(crop_type=GreenHouse.CropTypes.POTATOES)
        self.assertEqual(greenhouse_potatoes.crop_type, 'PT')

        # Case 3: option: default should be 'Tomatoes'
        default_greenhouse = GreenHouse()
        self.assertEqual(default_greenhouse.crop_type, 'TT')


class EnviromentTestCase(TestCase):
    
    def enviroment_creation(self):
        date = datetime(2023, 10, 17)
        temperature = 12
        air_humidity = 60
        light_level = 100
        PAR = 400
        co2_level = 500
        soil_moisture_level = 40
        soil_salinity = 1.5
        soil_temperature = 20
        weight_of_soil_and_plants = 1000
        stem_micro_Variability = 0.02
        
        obj = Enviroment.objects.create(
                                        date = date,
                                        temperature = temperature,
                                        air_humidity = air_humidity,
                                        light_level = light_level,
                                        PAR = PAR,
                                        co2_level = co2_level,
                                        soil_moisture_level = soil_moisture_level,
                                        soil_salinity = soil_salinity,
                                        soil_temperature = soil_temperature,
                                        weight_of_soil_and_plants = weight_of_soil_and_plants,
                                        stem_micro_Variability = stem_micro_Variability            
        )
        self.assertTrue(isinstance(obj, Enviroment))
        self.assertTrue(GreenHouse.objects.filter(
                                        date = date,
                                        temperature = temperature,
                                        air_humidity = air_humidity,
                                        light_level = light_level,
                                        PAR = PAR,
                                        co2_level = co2_level,
                                        soil_moisture_level = soil_moisture_level,
                                        soil_salinity = soil_salinity,
                                        soil_temperature = soil_temperature,
                                        weight_of_soil_and_plants = weight_of_soil_and_plants,
                                        stem_micro_Variability = stem_micro_Variability   
        )) 