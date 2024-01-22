import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphene_django import DjangoObjectType
from greenhouse_management.exceptions import PermissionDenied
from greenhouse_management.graphql.Location import LocationType
from greenhouse_management.graphql.User import UserType
from greenhouse_management.models import *


class GreenHouseType(DjangoObjectType):
    class Meta:
        model = GreenHouse
        fields = '__all__'
    location = graphene.Field(LocationType)
    owner = graphene.Field(UserType)
    authorized_users = list(graphene.Field(UserType))


class CropTypeEnum(graphene.Enum):
    TOMATOES = "TT"
    POTATOES = "PT"


class GreenHouseInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    crop_type = graphene.String
    location = graphene.ID
    authorized_users = graphene.List(graphene.ID)


class CreateGreenHouse(graphene.Mutation):
    """To create greenhouse provide 'name', 'crop_type', 'location, 'authorized_users' and 'owner'."""

    class Arguments:
        input = GreenHouseInput(required=True)

    greenhouse = graphene.Field(GreenHouseType)

    @classmethod
    @login_required
    def mutate(cls, root, info, input):
        request_user = info.context.user

        try:
            if request_user.is_superuser:
                location = Location.objects.get(id=input.location)
            else:
                location = Location.objects.get(id=input.location, owner=request_user)
        except Location.DoesNotExist:
            raise Exception("Location with this credentials does not exist.")
        

        greenhouse = GreenHouse.objects.create(
            name=input.name,
            crop_type=input.crop_type,
            location=location,
            owner=request_user
        )

        greenhouse.authorized_users.add(request_user)
        for authorized_user in input.authorized_users:
            try:         
                user = CustomUser.objects.get(id=authorized_user)
                greenhouse.authorized_users.add(user)
            except CustomUser.DoesNotExist:
                raise Exception("User with this credentials does not exist.")
        
        greenhouse.save()

        return CreateGreenHouse(greenhouse=greenhouse)
    

class UpdateGreenHouse(graphene.Mutation):
    """To update greenhouse change 'name', 'crop_type', 'location, 'authorized_users' and 'owner'."""
    class Arguments:
        input = GreenHouseInput(required=True)
        id = graphene.Int(required=True)

    greenhouse = graphene.Field(GreenHouseType)

    @classmethod
    @login_required
    def mutate(cls, root, info, input, id):
        greenhouse = GreenHouse.objects.get(pk=id)

        if info.context.user.is_superuser or info.context.user == greenhouse.owner:
            greenhouse.name = input.name if input.name not in ['', None] else greenhouse.name
            greenhouse.crop_type = input.crop_type if input.crop_type not in ['', None] else greenhouse.crop_type
            greenhouse.owner = greenhouse.owner

            if input.location:
                try:
                    location = Location.objects.get(pk=input.location)
                    if info.context.user.is_superuser or info.context.user == location.owner:
                        greenhouse.location = location
                    else:
                        greenhouse.location = greenhouse.location
                        raise Exception("The user is not the owner of the selected location")
                except Location.DoesNotExist:
                    raise Exception("Location with this credentials does not exist.")
            else:
                greenhouse.location = greenhouse.location

            if input.authorized_users:
                greenhouse.authorized_users.clear()
                greenhouse.authorized_users.add(info.context.user)
                for authorized_user in input.authorized_users:
                    try:         
                        user = CustomUser.objects.get(id=authorized_user)
                        greenhouse.authorized_users.add(user)
                    except CustomUser.DoesNotExist:
                        raise Exception("User with this credentials does not exist.")
            else:
                greenhouse.authorized_users = greenhouse.authorized_users
                
            greenhouse.save()
        else:
            raise PermissionDenied
        return UpdateGreenHouse(greenhouse=greenhouse)


class DeleteGreenHouse(graphene.Mutation):
    """To delete greenhouse you need to provide 'id'."""
    class Arguments:
        id = graphene.Int(required=True)

    greenhouse = graphene.Field(GreenHouseType)

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        greenhouse = GreenHouse.objects.get(pk=id)
        if info.context.user.is_superuser or info.context.user == greenhouse.owner:
            greenhouse.delete()
        else:
            raise PermissionDenied
        return None

class GreenHouseMutation(graphene.ObjectType):
    create_greenhouse = CreateGreenHouse.Field()
    update_greenhouse = UpdateGreenHouse.Field()
    delete_greenhouse = DeleteGreenHouse.Field()


class GreenHouseQuery(graphene.ObjectType):
    greenhouse = graphene.Field(GreenHouseType, id=graphene.Int(required=True))
    greenhouses = graphene.List(GreenHouseType)

    @login_required
    def resolve_greenhouse(root, info, id):
        request_user = info.context.user
        
        try:
            greenhouse = GreenHouse.objects.get(pk=id)
        except Location.DoesNotExist:
            raise Exception("GreenHouse with this name does not exist.")
        
        # Check if the user has permission to access the greenhouse
        if request_user.is_superuser or request_user in greenhouse.authorized_users:
            return greenhouse
        else:
            raise PermissionDenied

    @login_required
    def resolve_greenhouse(root, info):
        request_user = info.context.user

        if request_user.is_superuser:
            return Location.objects.all()
        else:
            return Location.objects.filter(owner=request_user)
