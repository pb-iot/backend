from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from greenhouse_management.models import GreenHouse
from greenhouse_management.models import Location
from greenhouse_management.models import Environment

create_greenhouse = '''mutation createGreenhouse($name: String!, $cropType: String!, $location: Int!){
    createGreenhouse(input: {name: $name, cropType: $cropType, location: $location}){
        greenhouse{
            name,
            cropType,
            location {
                id,
                name
            }
        }
    }
}'''

delete_greenhouse = '''mutation deleteGreenhouse($id: Int!){
    deleteGreenhouse(id: $id){
        greenhouse{
            name,
            cropType,
            location {
                id,
                name
            }
        }
    }
}'''

get_greenhouse = '''query getGreenhouse($id: Int!){
    greenhouse(id: $id){
        name,
        cropType,
        location {
            id,
            name
        }
    }
}'''

get_greenhouses = '''query {
    greenhouses{
        name,
        cropType,
        location {
            id,
            name
        }
    }
}'''

class GreenHouseTests(JSONWebTokenTestCase):
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

        self.location = location

        green_house = GreenHouse.objects.create(
            name="GreenHouse1",
            owner=self.user,
            location=self.location
        )

        Environment.objects.create(
            green_house=green_house,
            date="2023-01-02T12:00:00",
            temperature=25.00,
            air_humidity=60.00,
            light_level=500.00,
            par=150.00,
            co2_level=400.00,
            soil_moisture_level=40.00,
            soil_salinity=3.50,
            soil_temperature=20.00,
            weight_of_soil_and_plants=150.00,
            stem_micro_variability=0.20
        )

    def test_create_greenhouse(self):
        variables = {
            "name": "GreenHouse2",
            "cropType": "POTATOES",
            "location": 1,
        }

        executed = self.client.execute(create_greenhouse, variables)
        assert executed.data == {
            "createGreenHouse": {
                "greenhouse": {
                    "name": "GreenHouse2",
                    "cropType": "POTATOES",
                    "location": {
                        "id": "1",
                        "name": "test2"
                    }
                }
            }
        }

    def test_delete_greenhouse(self):
        variables = {
            "id": 1
        }

        executed = self.client.execute(delete_greenhouse, variables)
        assert "deleteGreenhouse" in executed.data and "greenhouse" in executed.data["deleteGreenhouse"]


    def test_get_greenhouse(self):
        variables = {
            "id": 1,
        }

        executed = self.client.execute(get_greenhouse, variables)
        assert executed.data == {
            "greenhouse": {
                "name": "GreenHouse1",
                "cropType": "TOMATOES",
                "location": {
                    "id": "1",
                    "name": "test2"
                }
            }
        }

    def test_get_greenhouses(self):
        executed = self.client.execute(get_greenhouses)
        assert executed.data == {
            "greenhouses": [{
                "name": "GreenHouse1",
                "cropType": "TOMATOES",
                "location": {
                    "id": "1",
                    "name": "test2"
                }
            }]
        }
