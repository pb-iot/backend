from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from greenhouse_management.models import CustomUser, GreenHouse
from greenhouse_management.models import Location

create_greenhouse = '''mutation createMutation($name: String!, $cropType: String!, $location: ID!, $authorizedUsers: [ID]){
                        createGreenhouse(input: {name: $name, cropType: $cropType, location: $location, authorizedUsers: $authorizedUsers}){
                            greenhouse{
                                name,
                                cropType,
                                location {
                                    id,
                                    name
                                },
                                owner {
                                    firstName,
                                    isSuperuser
                                },
                                authorizedUsers {
                                    firstName,
                                    isSuperuser
                                }
                            }
                        }
                    }'''

update_greenhouse = '''mutation updateMutation($name: String, $cropType: String, $location: ID, $authorizedUsers: [ID], $id: Int!){
                        updateGreenhouse(input: {name: $name, cropType: $cropType, location: $location, authorizedUsers: $authorizedUsers}, id: $id){
                            greenhouse{
                                name,
                                cropType,
                                location {
                                    id,
                                    name
                                },
                                owner {
                                    firstName,
                                    isSuperuser
                                },
                                authorizedUsers {
                                    firstName,
                                    isSuperuser
                                }
                            }
                        }
                    }'''

delete_greenhouse = '''mutation deleteMutation($id: Int!){
                        deleteGreenhouse(id: $id){
                            greenhouse{
                                name
                            }
                        }
                    }'''

get_greenhouse = '''query($id: Int!){
                        greenhouse(id: $id){
                            name,
                            cropType,
                            location {
                                id,
                                name
                            },
                            owner {
                                firstName,
                                isSuperuser
                            },
                            authorizedUsers {
                                firstName,
                                isSuperuser
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
                            },
                            owner {
                                firstName,
                                isSuperuser
                            },
                            authorizedUsers {
                                firstName,
                                isSuperuser
                            }
                        }
                    }'''

class GreenHouseTests(JSONWebTokenTestCase):
    def setUp(self):
        usual_user1 = CustomUser.objects.create_user(first_name="custom1", last_name="user1", password="njw#kncw22",
                                       email="def1@abc.com")
        usual_user2 = CustomUser.objects.create_user(first_name="custom2", last_name="user2", password="njw#kncw22",
                                       email="def2@abc.com")
        usual_user3 = CustomUser.objects.create_user(first_name="custom3", last_name="user3", password="njw#kncw22",
                                       email="def3@abc.com")
        self.user = get_user_model().objects.create_superuser(first_name="Jane", last_name="Doe", password="F3d3w8ddf",
                                                              email="default@abc.com")
        self.user.is_active = True
        self.user.save()
        self.client.authenticate(self.user)

        location = Location.objects.create(name="Bialystok", coordinates=(42.12345, -71.98765), owner=usual_user1)
        greenhouse1 = GreenHouse.objects.create(name="TestGreenHouse1", crop_type="TT", location=location, owner=usual_user1)
        greenhouse1.authorized_users.set([usual_user1, usual_user2, usual_user3])
        greenhouse2 = GreenHouse.objects.create(name="TestGreenHouse2", crop_type="PT", location=location, owner=usual_user3)
        greenhouse2.authorized_users.set([usual_user1, usual_user3])


    def test_create_greenhouse(self):
        variables = {
            "name": "TestGreenHouse3",
            "cropType": "PT",
            "location": 1,
            "authorizedUsers": [1, 3]
        }

        executed = self.client.execute(create_greenhouse, variables)
        assert executed.data == {
            "createGreenhouse": {
                "greenhouse": {
                    "name": "TestGreenHouse3",
                    "cropType": "PT",
                    "location": {
                        "id": "1",
                        "name": "Bialystok"
                    },
                    "owner": {
                        "firstName": "Jane",
                        "isSuperuser": True
                    },
                    "authorizedUsers": [{
                        "firstName": "custom1", 
                        "isSuperuser": False
                        }, {
                        "firstName": "custom3", 
                        "isSuperuser": False
                        }, {
                            "firstName": "Jane",
                            "isSuperuser": True
                        }
                    ]
                }
            }
        }


    def test_update_greenhouse(self):
        variables = {
            "id": 1,
            "name": "UpdateGreenHouse1",
            "cropType": "PT",
            "authorizedUsers": [2]
        }

        executed = self.client.execute(update_greenhouse, variables)
        assert executed.data == {
            "updateGreenhouse": {
                "greenhouse": {
                    "name": "UpdateGreenHouse1",
                    "cropType": "PT",
                    "location": {
                        "id": "1",
                        "name": "Bialystok"
                    },
                    "owner": {
                        "firstName": "custom1",
                        "isSuperuser": False
                    },
                    "authorizedUsers": [{
                        "firstName": "custom1", 
                        "isSuperuser": False
                        }, {
                        "firstName": "custom2", 
                        "isSuperuser": False
                        }
                    ]
                }
            }
        }


    def test_delete_greenhouse(self):
        variables = {
            "id": 2
        }

        executed = self.client.execute(delete_greenhouse, variables)
        assert executed.data == {
            "deleteGreenhouse": None
        }


    def test_get_greenhouse(self):
        variables = {
            "id": 1,
        }

        executed = self.client.execute(get_greenhouse, variables)
        assert executed.data == {
            "greenhouse": {
                "name": "TestGreenHouse1",
                "cropType": "TT",
                "location": {
                    "id": "1",
                    "name": "Bialystok"
                },
                "owner": {
                    "firstName": "custom1",
                    "isSuperuser": False
                },
                "authorizedUsers": [{
                    "firstName": "custom1", 
                    "isSuperuser": False
                    }, {
                    "firstName": "custom2", 
                    "isSuperuser": False
                    }, {
                    "firstName": "custom3", 
                    "isSuperuser": False
                    }
                ]
            }
        }


    def test_get_greenhouses(self):
        executed = self.client.execute(get_greenhouses)
        assert executed.data == {
            "greenhouses": [{
                "name": "TestGreenHouse1",
                "cropType": "TT",
                "location": {
                    "id": "1",
                    "name": "Bialystok"
                },
                "owner": {
                    "firstName": "custom1",
                    "isSuperuser": False
                },
                "authorizedUsers": [{
                    "firstName": "custom1", 
                    "isSuperuser": False
                    }, {
                    "firstName": "custom2", 
                    "isSuperuser": False
                    }, {
                    "firstName": "custom3", 
                    "isSuperuser": False
                    }
                ]
            }, {
                "name": "TestGreenHouse2",
                "cropType": "PT",
                "location": {
                    "id": "1",
                    "name": "Bialystok"
                },
                "owner": {
                    "firstName": "custom3",
                    "isSuperuser": False
                },
                "authorizedUsers": [{
                    "firstName": "custom1", 
                    "isSuperuser": False
                    }, {
                    "firstName": "custom3", 
                    "isSuperuser": False
                    }
                ]
            }]
        }
