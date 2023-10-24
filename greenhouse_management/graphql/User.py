import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
import graphql_jwt
from greenhouse_management.exceptions import PermissionDenied
from greenhouse_management.models import *


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        exclude = ['password',]


class ProtectedUserInput(graphene.InputObjectType):
    email = graphene.String()
    password = graphene.String()
    last_name = graphene.String()
    first_name = graphene.String()
    date_joined = graphene.DateTime()


class UserInput(ProtectedUserInput):
    is_superuser = graphene.Boolean()
    is_active = graphene.Boolean()
    is_staff = graphene.Boolean()


class CreateUser(graphene.Mutation):
    """To create user provide 'firstname', 'lastname', 'email', 'password'.
        is_active', 'is_staff' and 'is_superuser' is set in code.
        Other fields are optional."""

    class Arguments:
        input = UserInput(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def create_as_regular_user(cls, user_data):
        permission_locked_fields = ['is_staff', 'is_superuser', 'is_active']
        for field in permission_locked_fields:
            user_data.pop(field, None)

        user = CustomUser.objects.create_user(**user_data)
        return user

    @classmethod
    def create_as_superuser(cls, user_data):
        if user_data.get('is_superuser', None):
            user_data['is_staff'] = True
            return CustomUser.objects.create_superuser(**user_data)
        return CustomUser.objects.create_user(**user_data)

    @classmethod
    def mutate(cls, root, info, input):
        if info.context.user.is_superuser:
            user = cls.create_as_superuser(input)
        else:
            user = cls.create_as_regular_user(input)

        user.save()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    """To update user change 'first_name', 'last_name', 'email'.
        'is_active', 'is_staff' and 'is_superuser' is set only by superuser."""

    class Arguments:
        input = UserInput(required=True)
        id = graphene.Int(required=True)

    user = graphene.Field(UserType)

    @classmethod
    @login_required
    def mutate(cls, root, info, input, id):
        user = CustomUser.objects.get(pk=id)
        if info.context.user.is_superuser or info.context.user.id == id:
            user.first_name = input.first_name if input.first_name not in [
                '', None] else user.first_name
            user.last_name = input.last_name if input.last_name not in [
                '', None] else user.last_name
            user.email = input.email if input.email not in [
                '', None] else user.email

            if any(field == '' or field is not None for field in [input.is_active, input.is_superuser, input.is_staff]):
                if info.context.user.is_superuser:
                    user.is_active = input.is_active if input.is_active not in [
                        '', None] else user.is_active
                    user.is_superuser = input.is_superuser if input.is_superuser not in ['',
                                                                                         None] else user.is_superuser
                    user.is_staff = input.is_staff if input.is_staff not in [
                        '', None] else user.is_staff
                else:
                    raise PermissionDenied
        else:
            raise PermissionDenied

        user.save()
        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):
    """To delete user you need to provide 'id'."""

    class Arguments:
        id = graphene.Int(required=True)

    user = graphene.Field(UserType)

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        if info.context.user.is_superuser or info.context.user.id == id:
            user = CustomUser.objects.get(pk=id)
            user.is_active = False
            user.save()
        else:
            raise PermissionDenied

        return None


class ChangePassword(graphene.Mutation):
    """To change password provide all listed fields"""

    class Arguments:
        id = graphene.Int(required=True)
        old_password = graphene.String(required=True)
        new_password = graphene.String(required=True)
        repeat_password = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    @login_required
    def mutate(cls, root, info, id, old_password, new_password, repeat_password):
        if info.context.user.id == id:
            user = CustomUser.objects.get(pk=id)
            if not user.check_password(old_password):
                raise Exception("Incorrect old password")
            if new_password != repeat_password:
                raise Exception("Passwords are not the same")
            if old_password == new_password:
                raise Exception("You must enter a new password")

            user.set_password(new_password)
            user.save()
        else:
            raise PermissionDenied

        return ChangePassword(user=user)


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        if not info.context.user.is_active:
            raise Exception("Account is not active")
        return cls(user=info.context.user)


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    change_password = ChangePassword.Field()

    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


class UserQuery(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    users = graphene.List(UserType)

    @login_required
    def resolve_user(root, info, id):
        try:
            user = CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            raise Exception("User with this credentials does not exist.")

        if not user.is_active:
            raise Exception("User is inactive")

        return user

    @login_required
    def resolve_users(root, info):
        request_user = info.context.user

        if request_user.is_superuser:
            return CustomUser.objects.all()
        else:
            return CustomUser.objects.filter(is_active=True)
