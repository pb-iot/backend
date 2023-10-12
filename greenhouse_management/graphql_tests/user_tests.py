from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from greenhouse_management.models import *

create_user = '''mutation createMutation($firstName: String!, $lastName: String!, $password: String!, $email: String!){
                      createUser(input: {firstName: $firstName, lastName: $lastName, password: $password, email: $email}){
                        user{
                          firstName,
                          isSuperuser
                        }
                      }
                    }'''

create_superuser = '''mutation createMutation($firstName: String!, $password: String!, $forStaff: Boolean, $email: String!){
                      createUser(input: {firstName: $firstName, password: $password, email: $email}, forStaff:$forStaff){
                        user{
                          firstName,
                          isSuperuser
                        }
                      }
                    }'''

update_user = '''mutation updateMutation($firstName: String!, $lastName: String!, $id: Int!){
                      updateUser(input: {firstName: $firstName, lastName: $lastName}, id: $id){
                        user{
                          firstName,
                          lastName
                        }
                      }
                    }'''

delete_user = '''mutation deleteMutation($id: Int!){
                      deleteUser(id: $id){
                        user{
                          firstName,
                          lastName
                        }
                      }
                    }'''

change_password = '''mutation updateMutation($oldPassword: String!, $newPassword: String!, $repeatPassword: String!, $id: Int!){
                      changePassword(oldPassword: $oldPassword, newPassword: $newPassword, repeatPassword: $repeatPassword, id: $id){
                        user{
                          firstName,
                          lastName
                        }
                      }
                    }'''

get_user = '''query($id: Int!){   
                  user(id: $id){
                    firstName,
                    lastName
                  }
                }'''

get_users = '''query{   
                  users{
                    firstName,
                    lastName
                  }
                }'''


class SuperUserTests(JSONWebTokenTestCase):
    def setUp(self):
        CustomUser.objects.create_user(first_name="custom", last_name="user", password="njw#kncw22",
                                       email="def@abc.com")
        self.user = get_user_model().objects.create_superuser(first_name="Jane", last_name="Doe", password="F3d3w8ddf",
                                                              email="default@abc.com")
        self.user.is_active = True
        self.user.save()
        self.client.authenticate(self.user)

    def test_create_admin(self):
        variables = {
            "firstName": "test",
            "lastName": "admin",
            "password": "egi8654G4",
            "forStaff": True,
            "email": "default2@abc.com"
        }

        executed = self.client.execute(create_superuser, variables)
        assert executed.data == {
            "createUser": {
                "user": {
                    "firstName": "test",
                    "isSuperuser": True
                }
            }
        }

    def test_update_user(self):
        variables = {
            "id": 1,
            "firstName": "changed",
            "lastName": "data"
        }

        executed = self.client.execute(update_user, variables)
        assert executed.data == {
            "updateUser": {
                "user": {
                    "firstName": "changed",
                    "lastName": "data"
                }
            }
        }

    def test_delete_user(self):
        variables = {
            "id": 1
        }

        executed = self.client.execute(delete_user, variables)
        assert executed.data == {
            "deleteUser": None
        }

    def test_change_password(self):
        variables = {
            "id": 2,
            "oldPassword": "F3d3w8ddf",
            "newPassword": "tvf334Ff",
            "repeatPassword": "tvf334Ff"
        }

        executed = self.client.execute(change_password, variables)
        print(executed)
        assert executed.data == {
            "changePassword": {
                "user": {
                    "firstName": "Jane",
                    "lastName": "Doe"
                }
            }
        }

    def test_get_user(self):
        variables = {
            "id": 1,
        }

        executed = self.client.execute(get_user, variables)
        assert executed.data == {
            "user": {
                "firstName": "custom",
                "lastName": "user"
            }
        }

    def test_get_all_users(self):
        executed = self.client.execute(get_users)
        assert executed.data == {
            "users": [{
                "firstName": "custom",
                "lastName": "user"
            }, {
                "firstName": "Jane",
                "lastName": "Doe"
            }]
        }


class UsersTests(JSONWebTokenTestCase):
    def setUp(self):
        CustomUser.objects.create_user(first_name="custom", last_name="user", password="njw#kncw22",
                                       email="def@abc.com")
        self.user = get_user_model().objects.create_user(first_name="Jane", last_name="Doe", password="jhgc28dxh",
                                                         email="default@abc.com")
        self.user.is_active = True
        self.user.save()
        self.client.authenticate(self.user)

    def test_update_user(self):
        variables = {
            "id": 2,
            "firstName": "changed",
            "lastName": "data"
        }

        executed = self.client.execute(update_user, variables)
        assert executed.data == {
            "updateUser": {
                "user": {
                    "firstName": "changed",
                    "lastName": "data"
                }
            }
        }

    def test_update_another_user(self):
        variables = {
            "id": 1,
            "firstName": "John",
            "lastName": "Doe"
        }
        executed = self.client.execute(update_user, variables)
        assert executed.errors[0].message == \
               'You do not have the required permissions to perform this action'

    def test_delete_user_no_permission(self):
        variables = {
            "id": 1
        }

        executed = self.client.execute(delete_user, variables)
        assert executed.errors[0].message == \
               'You do not have the required permissions to perform this action'

    def test_delete_user(self):
        variables = {
            "id": 2
        }
        executed = self.client.execute(delete_user, variables)
        assert executed.data.popitem()[1] is None

    def test_change_password_not_the_same(self):
        variables = {
            "id": 2,
            "oldPassword": "jhgc28dxh",
            "newPassword": "tvf334Ff",
            "repeatPassword": "avf334Ff"
        }

        executed = self.client.execute(change_password, variables)
        assert executed.errors[0].message == 'Passwords are not the same'

    def test_change_password_incorrect(self):
        variables = {
            "id": 2,
            "oldPassword": "xdcsdlos",
            "newPassword": "jhgc28dxh",
            "repeatPassword": "drtyo8765"
        }

        executed = self.client.execute(change_password, variables)
        assert executed.errors[0].message == 'Incorrect old password'

    def test_change_password_new_equal_old(self):
        variables = {
            "id": 2,
            "oldPassword": "jhgc28dxh",
            "newPassword": "jhgc28dxh",
            "repeatPassword": "jhgc28dxh"
        }

        executed = self.client.execute(change_password, variables)
        assert executed.errors[0].message == 'You must enter a new password'

    def test_change_password_no_permission(self):
        variables = {
            "id": 1,
            "oldPassword": "xdfghjki",
            "newPassword": "345678xhbs",
            "repeatPassword": "345678xhbs"
        }

        executed = self.client.execute(change_password, variables)
        assert executed.errors[0].message == \
               'You do not have the required permissions to perform this action'

    def test_get_user(self):
        inactive_user = CustomUser.objects.create_user(first_name="John", last_name="Doe", password="Adgvwey25f",
                                                       email="default2@aa.com")

        inactive_user.is_active = False
        inactive_user.save()

        variables = {
            "id": 3,
        }

        executed = self.client.execute(get_user, variables)
        assert executed.errors[0].message == 'User is inactive'
