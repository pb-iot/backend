import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphene_django import DjangoObjectType
from greenhouse_management.exceptions import PermissionDenied
from greenhouse_management.models import *


class GreenHouseType(DjangoObjectType):
    class Meta:
        model = GreenHouse
        fields = '__all__'

class GreenHouseInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    crop_type = graphene.String
    location_id = graphene.ID

class CreateGreenHouse(graphene.Mutation):

    class Arguments:
        input = GreenHouseInput(required=True)

    greenhouse = graphene.Field(GreenHouseType)

    @classmethod
    @login_required
    def mutate(cls, root, info, input):
        #location = Location.objects.get(pk=input.location_id)

        greenhouse = GreenHouse.objects.create(
            name=input.name,
            crop_type=input.crop_type,
            #location=location,
            owner=info.context.user
        )

        greenhouse.authorized_users.add(info.context.user)
        greenhouse.save()

        return CreateGreenHouse(greenhouse=greenhouse)
    

class UpdateGreenHouse(graphene.Mutation):
    class Arguments:
        input = GreenHouseInput(required=True)
        id = graphene.Int(required=True)

    greenhouse = graphene.Field(GreenHouseType)

    @classmethod
    @login_required
    def mutate(cls, root, info, input, id):
        greenhouse = GreenHouse.objects.get(pk=id)

        # Check if the user has permission to update the greenhouse
        if info.context.user.is_superuser or info.context.user == greenhouse.owner:
            location = Location.objects.get(pk=input.location_id)
            greenhouse.name = input.name
            greenhouse.crop_type = input.crop_type
            greenhouse.location = location
            greenhouse.save()
        else:
            raise PermissionDenied
        return UpdateGreenHouse(greenhouse=greenhouse)


class DeleteGreenHouse(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    greenhouse = graphene.Field(GreenHouseType)

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        greenhouse = GreenHouse.objects.get(pk=id)

        # Check if the user has permission to delete the greenhouse
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
        if request_user.is_superuser or request_user == greenhouse.owner:
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
