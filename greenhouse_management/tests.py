from django.test import TestCase
from .models import Localization


class LocalizationTestCase(TestCase):

    def create_localization(self, name="Bialystok"):
        return Localization.objects.create(name=name)
    
    def test_localization_creation(self):
        obj = self.create_localization()
        self.assertTrue(isinstance(obj, Localization))
        self.assertTrue(Localization.objects.filter(name="Bialystok").exists())
    

