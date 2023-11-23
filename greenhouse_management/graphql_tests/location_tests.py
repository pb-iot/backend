from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from greenhouse_management.models import *

create_location = '''mutation createMutation($name: String!, $lat: Float!, $lon: Float!){
                      createLocation(input: {name: $name, lat: $lat, lon: $lon}){
                        location{
                          name,
                          owner{
                            firstName
                          },
                        }
                      }
                    }'''

update_location = '''mutation updateMutation($name: String, $lat: Float, $lon: Float, $id: Int!){
                      updateLocation(input: {name: $name, lat: $lat, lon: $lon}, id: $id){
                        location{
                          name,
                          coordinates
                        }
                      }
                    }'''

delete_location = '''mutation deleteMutation($id: Int!){
                      deleteLocation(id: $id){
                        location{
                          name
                        }
                      }
                    }'''

get_location = '''query($id: Int!){   
                  location(id: $id){
                    name,
                    coordinates
                  }
                }'''

get_locations = '''query{   
                  locations{
                    name,
                    coordinates
                  }
                }'''


class SuperUserTests(JSONWebTokenTestCase):
    def setUp(self):
        usual_user = CustomUser.objects.create_user(first_name="custom", last_name="user", password="njw#kncw22",
                                       email="def@abc.com")
        self.user = get_user_model().objects.create_superuser(first_name="Jane", last_name="Doe", password="F3d3w8ddf",
                                                              email="default@abc.com")
        self.user.is_active = True
        self.user.save()
        self.client.authenticate(self.user)

        Location.objects.create(name="test2", coordinates=[40.0, 48.2], owner=usual_user)

    def test_create_location(self):
        variables = {
            "name": "test",
            "lat": 10.0,
            "lon": 15.8
        }

        executed = self.client.execute(create_location, variables)
        assert executed.data == {
            "createLocation": {
                "location": {
                    "name": "test",
                    "owner": {
                        "firstName": "Jane"
                    },
                }
            }
        }

    def test_update_location(self):
        variables = {
            "id": 1,
            "lat": 20.9
        }

        executed = self.client.execute(update_location, variables)
        assert executed.data == {
            "updateLocation": {
                "location": {
                    "name": "test2",
                    "coordinates": "20.9, 48.2"
                }
            }
        }

    def test_delete_location(self):
        variables = {
            "id": 1
        }

        executed = self.client.execute(delete_location, variables)
        assert executed.data == {
            "deleteLocation": None
        }

    def test_get_location(self):
        variables = {
            "id": 1,
        }

        executed = self.client.execute(get_location, variables)
        assert executed.data == {
            "location": {
                "name": "test2",
                "coordinates": "40.0, 48.2"
            }
        }

    def test_get_locations(self):
        executed = self.client.execute(get_locations)
        assert executed.data == {
            "locations": [{
                "name": "test2",
                "coordinates": "40.0, 48.2"
            }]
        }


class UsersTests(JSONWebTokenTestCase):
    def setUp(self):
        usual_user = CustomUser.objects.create_user(first_name="custom", last_name="user", password="njw#kncw22",
                                       email="def@abc.com")
        self.user = get_user_model().objects.create_user(first_name="Jane", last_name="Doe", password="jhgc28dxh",
                                                         email="default@abc.com")
        self.user.is_active = True
        self.user.save()
        self.client.authenticate(self.user)

        Location.objects.create(name="test2", coordinates=[40.0, 48.2], owner=usual_user)
        Location.objects.create(name="test3", coordinates=[90.0, 21.8], owner=self.user)

    def test_update_location(self):
        variables = {
            "id": 2,
            "name": "changed"
        }

        executed = self.client.execute(update_location, variables)
        assert executed.data == {
            "updateLocation": {
                "location": {
                    "name": "changed",
                    "coordinates": "90.0, 21.8"
                }
            }
        }

    def test_update_another_location(self):
        variables = {
            "id": 1,
            "name": "changed"
        }
        executed = self.client.execute(update_location, variables)
        assert executed.errors[0].message == \
            'You do not have the required permissions to perform this action'

    def test_delete_location_no_permission(self):
        variables = {
            "id": 1
        }

        executed = self.client.execute(delete_location, variables)
        assert executed.errors[0].message == \
            'You do not have the required permissions to perform this action'

    def test_delete_location(self):
        variables = {
            "id": 2
        }
        executed = self.client.execute(delete_location, variables)
        assert executed.data.popitem()[1] is None

    def test_get_location(self):
        variables = {
            "id": 2,
        }

        executed = self.client.execute(get_location, variables)
        assert executed.data == {
            "location": {
                "name": "test3",
                "coordinates": "90.0, 21.8"
            }
        }

    def test_get_another_location(self):
        variables = {
            "id": 1,
        }

        executed = self.client.execute(get_location, variables)
        assert executed.errors[0].message == \
               'You do not have the required permissions to perform this action'
