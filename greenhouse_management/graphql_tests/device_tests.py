from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from greenhouse_management.models import *

create_device = '''mutation createMutation($name: String!, $functionality: String!, $greenhouse: ID!){
                      createDevice(input: {name: $name, functionality: $functionality, greenhouse: $greenhouse}){
                        device{
                          name,
                          functionality,
                          greenhouse{
                            id,
                            name
                          }
                        }
                      }
                    }'''

update_device = '''mutation updateMutation($name: String, $functionality: String, $greenhouse: ID, $id: Int!){
                      updateDevice(input: {name: $name, functionality: $functionality, greenhouse: $greenhouse}, id: $id){
                        device{
                          name,
                          functionality,
                          greenhouse{
                            id,
                            name
                          }
                        }
                      }
                    }'''

delete_device= '''mutation deleteMutation($id: Int!){
                      deleteDevice(id: $id){
                        device{
                          name
                        }
                      }
                    }'''

get_device = '''query($id: Int!){   
                  device(id: $id){
                    name,
                    functionality,
                    greenhouse{
                      id,
                      name
                    }
                  }
                }'''

get_devices = '''query{   
                  devices{
                    name,
                    functionality,
                    greenhouse{
                      id,
                      name
                    }
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

        location = Location.objects.create(name="Bialystok", coordinates=(42.12345, -71.98765), owner=usual_user)
        greenhouse1 = GreenHouse.objects.create(name="TestGreenHouse1", location=location, owner=usual_user)
        greenhouse2 = GreenHouse.objects.create(name="TestGreenHouse2", location=location, owner=usual_user)
        Device.objects.create(name="test", functionality="AC", greenhouse=greenhouse1)
        Device.objects.create(name="test2", functionality="PA", greenhouse=greenhouse2)

    def test_create_device(self):
        variables = {
            "name": "test3",
            "functionality": "PA",
            "greenhouse": "1"
        }

        executed = self.client.execute(create_device, variables)
        assert executed.data == {
            "createDevice": {
                "device": {
                    "name": "test3",
                    "functionality": "PA",
                    "greenhouse": {
                        "id": "1",
                        "name": "TestGreenHouse1"
                    }
                }
            }
        }

    def test_update_device(self):
        variables = {
            "id": 1,
            "name": "testUpdate",
            "greenhouse": "2"
        }

        executed = self.client.execute(update_device, variables)
        assert executed.data == {
            "updateDevice": {
                "device": {
                    "name": "testUpdate",
                    "functionality": "AC",
                    "greenhouse": {
                        "id": "2",
                        "name": "TestGreenHouse2"
                    }
                }
            }
        }

    def test_delete_device(self):
        variables = {
            "id": 1
        }

        executed = self.client.execute(delete_device, variables)
        assert executed.data == {
            "deleteDevice": None
        }

    def test_get_device(self):
        variables = {
            "id": 2,
        }

        executed = self.client.execute(get_device, variables)
        assert executed.data == {
            "device": {
                "name": "test2",
                "functionality": "PA",
                "greenhouse": {
                    "id": "2",
                    "name": "TestGreenHouse2"
                }
            }
        }

    def test_get_devices(self):
        executed = self.client.execute(get_devices)
        assert executed.data == {
            "devices": [{
                "name": "test",
                "functionality": "AC",
                "greenhouse": {
                    "id": "1",
                    "name": "TestGreenHouse1"
                }
            }, {
                "name": "test2",
                "functionality": "PA",
                "greenhouse": {
                    "id": "2",
                    "name": "TestGreenHouse2"
                }
            }]
        }