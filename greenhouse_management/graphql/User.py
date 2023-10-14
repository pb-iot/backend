import graphene
from graphene_django import DjangoObjectType

from greenhouse_management.exceptions import PermissionDenied
from greenhouse_management.models import *


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserInput(graphene.InputObjectType):
    email = graphene.String()
    password = graphene.String()
    last_name = graphene.String()
    first_name = graphene.String()
    date_joined = graphene.DateTime()
    is_superuser = graphene.Boolean()
    is_active = graphene.Boolean()
    is_staff = graphene.Boolean()


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)
        for_staff = graphene.Boolean()

    user = graphene.Field(UserType)

    __doc__ = '''To create user provide 'firstname', 'lastname', 'email', 'password'. 
                'is_active', 'is_staff' and 'is_superuser' is set in code. 
                Other fields are optional.'''

    @classmethod
    def mutate(cls, root, info, input, for_staff=False):
        if info.context.user.is_superuser and for_staff:
            user = CustomUser.objects.create_superuser(**input)
        else:
            user = CustomUser.objects.create_user(**input)

        user.save()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)
        id = graphene.Int(required=True)

    user = graphene.Field(UserType)

    __doc__ = '''To update user change 'first_name', 'last_name', 'email'. 
                'is_active', 'is_staff' and 'is_superuser' is set only by superuser.'''

    @classmethod
    def mutate(cls, root, info, input, id):
        user = CustomUser.objects.get(pk=id)
        if info.context.user.is_superuser or info.context.user.id == id:
            user.first_name = input.first_name if input.first_name not in ['', None] else user.first_name
            user.last_name = input.last_name if input.last_name not in ['', None] else user.last_name
            user.email = input.email if input.email not in ['', None] else user.email

            if any(field == '' or field is not None for field in [input.is_active, input.is_superuser, input.is_staff]):
                if info.context.user.is_superuser:
                    user.is_active = input.is_active if input.is_active not in ['', None] else user.is_active
                    user.is_superuser = input.is_superuser if input.is_superuser not in ['',
                                                                                         None] else user.is_superuser
                    user.is_staff = input.is_staff if input.is_staff not in ['', None] else user.is_staff
                else:
                    raise PermissionDenied
        else:
            raise PermissionDenied

        user.save()
        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    user = graphene.Field(UserType)

    __doc__ = "To delete user you need to provide 'id'."

    @classmethod
    def mutate(cls, root, info, id):
        if info.context.user.is_superuser or info.context.user.id == id:
            user = CustomUser.objects.get(pk=id)
            user.is_active = False
            user.save()
        else:
            raise PermissionDenied

        return None


class ChangePassword(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        old_password = graphene.String(required=True)
        new_password = graphene.String(required=True)
        repeat_password = graphene.String(required=True)

    user = graphene.Field(UserType)

    __doc__ = "To change password provide all listed fields"

    @classmethod
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


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    change_password = ChangePassword.Field()


class UserQuery(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    users = graphene.List(UserType)

    def resolve_user(root, info, id):
        try:
            user = CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            raise Exception("User with this credentials does not exist.")

        if not user.is_active:
            raise Exception("User is inactive")

        return user

    def resolve_users(root, info):
        request_user = info.context.user

        if request_user.is_superuser:
            return CustomUser.objects.all()
        else:
            return CustomUser.objects.filter(is_active=True)
