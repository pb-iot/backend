from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from greenhouse_management.models import *

create_environment = '''mutation createEnvironment($greenhouse: Int!, $date: DateTime!, $temperature: Decimal!, $airHumidity: Decimal!, $lightLevel: Decimal!, $par: Decimal!, $co2Level: Decimal!, $soilMoistureLevel: Decimal!, $soilSalinity: Decimal!, $soilTemperature: Decimal!, $weightOfSoilAndPlants: Decimal!, $stemMicroVariability: Decimal!){
    createEnvironment(input: {greenhouse: $greenhouse, date: $date, temperature: $temperature, airHumidity: $airHumidity, lightLevel: $lightLevel, par: $par, co2Level: $co2Level, soilMoistureLevel: $soilMoistureLevel, soilSalinity: $soilSalinity, soilTemperature: $soilTemperature, weightOfSoilAndPlants: $weightOfSoilAndPlants, stemMicroVariability: $stemMicroVariability
    }){
        environment{
            date,
            temperature,
            airHumidity,
            lightLevel,
            par,
            co2Level,
            soilMoistureLevel,
            soilSalinity,
            soilTemperature,
            weightOfSoilAndPlants,
            stemMicroVariability
        }
    }
}'''

delete_environment = '''mutation deleteEnvironment($id: Int!){
    deleteEnvironment(id: $id){
        environment{
            date,
            temperature,
            airHumidity,
            lightLevel,
            par,
            co2Level,
            soilMoistureLevel,
            soilSalinity,
            soilTemperature,
            weightOfSoilAndPlants,
            stemMicroVariability
        }
    }
}'''

get_environment = '''query getEnvironment($id: Int!){
    environment(id: $id){
        date,
        temperature,
        airHumidity,
        lightLevel,
        par,
        co2Level,
        soilMoistureLevel,
        soilSalinity,
        soilTemperature,
        weightOfSoilAndPlants,
        stemMicroVariability
    }
}'''

get_environments = '''query {
    environments{
        date,
        temperature,
        airHumidity,
        lightLevel,
        par,
        co2Level,
        soilMoistureLevel,
        soilSalinity,
        soilTemperature,
        weightOfSoilAndPlants,
        stemMicroVariability
    }
}'''


class EnvironmentTests(JSONWebTokenTestCase):
    def setUp(self):
        usual_user = get_user_model().objects.create_user(
            first_name="custom", last_name="user", password="njw#kncw22", email="def@abc.com"
        )
        self.user = get_user_model().objects.create_user(
            first_name="Jane", last_name="Doe", password="jhgc28dxh", email="default@abc.com"
        )
        self.user.is_active = True
        self.user.save()
        self.client.authenticate(self.user)

        location = Location.objects.create(name="test2", coordinates=[40.0, 48.2], owner=usual_user)
        green_house = GreenHouse.objects.create(name="GreenHouse1", owner=self.user, location=location)
        Environment.objects.create(green_house=green_house, date="2023-01-02T12:00:00", temperature=25.00,
                                   air_humidity=60.00,
                                   light_level=500.00, par=150.00, co2_level=400.00, soil_moisture_level=40.00,
                                   soil_salinity=3.50, soil_temperature=20.00, weight_of_soil_and_plants=150.00,
                                   stem_micro_variability=0.20)

    def test_create_environment(self):
        variables = {
            "greenhouse": 1,
            "date": "2023-01-01T12:00:00",
            "temperature": 36.00,
            "airHumidity": 120.00,
            "lightLevel": 100.00,
            "par": 200.00,
            "co2Level": 40.00,
            "soilMoistureLevel": 4.00,
            "soilSalinity": 9.50,
            "soilTemperature": 40.00,
            "weightOfSoilAndPlants": 160.00,
            "stemMicroVariability": 1.5,
        }

        executed = self.client.execute(create_environment, variables)
        assert executed.data == {
            "createEnvironment": {
                "environment": {
                    "date": "2023-01-01T12:00:00",
                    "temperature": "36",
                    "airHumidity": "120",
                    "lightLevel": "100",
                    "par": "200",
                    "co2Level": "40",
                    "soilMoistureLevel": "4",
                    "soilSalinity": "9.5",
                    "soilTemperature": "40",
                    "weightOfSoilAndPlants": "160",
                    "stemMicroVariability": "1.5"}
            }
        }

    def test_delete_environment(self):
        variables = {
            "id": 1
        }

        executed = self.client.execute(delete_environment, variables)
        assert executed.data.popitem()[1] is None

    def test_get_environment(self):
        variables = {
            "id": 1,
        }

        executed = self.client.execute(get_environment, variables)
        assert executed.data == {
            "environment": {
                "date": "2023-01-02T12:00:00+00:00",
                "temperature": "25.00",
                "airHumidity": "60.00",
                "lightLevel": "500.00",
                "par": "150.00",
                "co2Level": "400.00",
                "soilMoistureLevel": "40.00",
                "soilSalinity": "3.50",
                "soilTemperature": "20.00",
                "weightOfSoilAndPlants": "150.00",
                "stemMicroVariability": "0.20",
            }
        }

    def test_get_environments(self):
        executed = self.client.execute(get_environments)
        assert executed.data == {
            "environments": [{
                "date": "2023-01-02T12:00:00+00:00",
                "temperature": "25.00",
                "airHumidity": "60.00",
                "lightLevel": "500.00",
                "par": "150.00",
                "co2Level": "400.00",
                "soilMoistureLevel": "40.00",
                "soilSalinity": "3.50",
                "soilTemperature": "20.00",
                "weightOfSoilAndPlants": "150.00",
                "stemMicroVariability": "0.20",
            }]
        }
