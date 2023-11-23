import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from greenhouse_management.exceptions import PermissionDenied
from greenhouse_management.models import *


class LocationType(DjangoObjectType):
    class Meta:
        model = Location
        fields = '__all__'

    def resolve_coordinates(self, info):
        return f"{str(self.coordinates[0])}, {str(self.coordinates[1])}"

class LocationInput(graphene.InputObjectType):
    name = graphene.String()
    lat = graphene.Float()
    lon = graphene.Float()


class CreateLocation(graphene.Mutation):
    """To create location provide 'name', 'lat' and 'lon'."""

    class Arguments:
        input = LocationInput(required=True)

    location = graphene.Field(LocationType)

    @classmethod
    @login_required
    def mutate(cls, root, info, input):
        location = Location.objects.create(name=input.name, coordinates=(input.lat, input.lon), owner=info.context.user)
        location.save()
        return CreateLocation(location=location)


class UpdateLocation(graphene.Mutation):
    """To update location change 'name', 'lat' and 'lon'."""

    class Arguments:
        input = LocationInput(required=True)
        id = graphene.Int(required=True)

    location = graphene.Field(LocationType)

    @classmethod
    @login_required
    def mutate(cls, root, info, input, id):
        location = Location.objects.get(pk=id)
        if info.context.user.is_superuser or info.context.user == location.owner:
            location.name = input.name if input.name not in ['', None] else location.name
            if input.lat is not None:
                location.coordinates = (input.lat, location.coordinates[1])
            if input.lon is not None:
                location.coordinates = (location.coordinates[0], input.lon)
            location.save()
        else:
            raise PermissionDenied
        return UpdateLocation(location=location)


class DeleteLocation(graphene.Mutation):
    """To delete location you need to provide 'id'."""

    class Arguments:
        id = graphene.Int(required=True)

    location = graphene.Field(LocationType)

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        location = Location.objects.get(pk=id)
        if info.context.user.is_superuser or info.context.user == location.owner:
            location.delete()
        else:
            raise PermissionDenied
        return None


class LocationMutation(graphene.ObjectType):
    create_location = CreateLocation.Field()
    update_location = UpdateLocation.Field()
    delete_location = DeleteLocation.Field()


class LocationQuery(graphene.ObjectType):
    location = graphene.Field(LocationType, id=graphene.Int(required=True))
    locations = graphene.List(LocationType)

    @login_required
    def resolve_location(root, info, id):
        request_user = info.context.user

        try:
            location = Location.objects.get(pk=id)
        except Location.DoesNotExist:
            raise Exception("Location with this credentials does not exist.")

        if request_user.is_superuser or request_user == location.owner:
            return location
        else:
            raise PermissionDenied

    @login_required
    def resolve_locations(root, info):
        request_user = info.context.user

        if request_user.is_superuser:
            return Location.objects.all()
        else:
            return Location.objects.filter(owner=request_user)
