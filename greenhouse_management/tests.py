from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Localization, GreenHouse


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
        crop_type = "StrrawBerries"
        User = get_user_model()
        owner_user =  User.objects.create_user(
            email='owner@user.com', password='foo')
        user_1 =  User.objects.create_user(
            email='normal1@user.com', password='foo')
        user_2 =  User.objects.create_user(
            email='normal2@user.com', password='foo')
        owner = owner_user
        authorized_users = [user_1, user_2]
        location = Localization.objects.create(name= "Bialystok")
        # environment <-- add test
        # devices <-- add test
        # default_environment <-- add test
        # environments <-- add test

        obj = GreenHouse.objects.create(name= name,
                                        crop_type= crop_type,
                                        location= location,
                                        owner= owner)
        obj.authorized_users.set(authorized_users)
        
        self.assertTrue(isinstance(obj, GreenHouse))
        self.assertTrue(GreenHouse.objects.filter(name= name, 
                                                  crop_type= crop_type,
                                                  location= location,
                                                  authorized_users__in= [user_1.id, user_2.id],
                                                  owner= owner).exists())
