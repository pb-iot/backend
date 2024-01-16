from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from greenhouse_management.models import *

create_greenhouse = '''
    mutation createMutation($name: String!){
        createGreenhouse(input: {name: $name}) {
            greenhouse {
                name
                owner {
                    firstName
                }
            }
        }
    }
'''

update_greenhouse = '''
    mutation updateMutation($name: String, $id: Int!){
        updateGreenhouse(input: {name: $name}, id: $id) {
            greenhouse {
                name
            }
        }
    }
'''

delete_greenhouse = '''
    mutation deleteMutation($id: Int!){
        deleteGreenhouse(id: $id) {
            greenhouse {
                name
            }
        }
    }
'''

get_greenhouse = '''
    query($id: Int!){
        greenhouse(id: $id) {
            name
        }
    }
'''

get_greenhouses = '''
    query {
        greenhouses {
            name
        }
    }
'''

class GreenHouseCRUDTests(JSONWebTokenTestCase):
    def setUp(self):
        usual_user = CustomUser.objects.create_user(first_name="custom", last_name="user", password="njw#kncw22",
                                                    email="def@abc.com")
        self.superuser = CustomUser.objects.create_superuser(first_name="Jane", last_name="Doe", password="F3d3w8ddf",
                                                             email="default@abc.com")
        self.superuser.is_active = True
        self.superuser.save()
        self.client.authenticate(self.superuser)

        GreenHouse.objects.create(name="test2", owner=usual_user)

    def test_create_greenhouse(self):
        variables = {
            "name": "test"
        }

        response = self.client.execute(create_greenhouse, variables)
        assert response.data == {
            "createGreenhouse": {
                "greenhouse": {
                    "name": "test",
                    "owner": {
                        "firstName": "Jane"
                    },
                }
            }
        }

    def test_update_greenhouse(self):
        variables = {
            "id": 1,
            "name": "changed"
        }

        response = self.client.execute(update_greenhouse, variables)
        assert response.data == {
            "updateGreenhouse": {
                "greenhouse": {
                    "name": "changed"
                }
            }
        }

    def test_delete_greenhouse(self):
        variables = {
            "id": 1
        }

        response = self.client.execute(delete_greenhouse, variables)
        assert response.data == {
            "deleteGreenhouse": None
        }

    def test_get_greenhouse(self):
        variables = {
            "id": 1
        }

        response = self.client.execute(get_greenhouse, variables)
        assert response.data == {
            "greenhouse": {
                "name": "test2"
            }
        }

    def test_get_greenhouses(self):
        response = self.client.execute(get_greenhouses)
        assert response.data == {
            "greenhouses": [{
                "name": "test2"
            }]
        }