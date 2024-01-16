import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from greenhouse_management.exceptions import PermissionDenied
from greenhouse_management.models import *
from django.db.models import Q


class EnvironmentType(DjangoObjectType):
    class Meta:
        model = Environment
        fields = '__all__'


class EnvironmentInput(graphene.InputObjectType):
    greenhouse = graphene.Int()
    date = graphene.DateTime()
    temperature = graphene.Decimal(max_digits=5, decimal_places=2)
    air_humidity = graphene.Decimal(max_digits=5, decimal_places=2)
    light_level = graphene.Decimal(max_digits=5, decimal_places=2)
    par = graphene.Decimal(max_digits=5, decimal_places=2)
    co2_level = graphene.Decimal(max_digits=5, decimal_places=2)
    soil_moisture_level = graphene.Decimal(max_digits=5, decimal_places=2)
    soil_salinity = graphene.Decimal(max_digits=5, decimal_places=2)
    soil_temperature = graphene.Decimal(max_digits=5, decimal_places=2)
    weight_of_soil_and_plants = graphene.Decimal(max_digits=8, decimal_places=2)
    stem_micro_variability = graphene.Decimal(max_digits=5, decimal_places=2)


class CreateEnvironment(graphene.Mutation):
    """To create environment provide all parameters."""

    class Arguments:
        input = EnvironmentInput(required=True)

    environment = graphene.Field(EnvironmentType)

    @classmethod
    #@login_required
    def mutate(cls, root, info, input):
        try:
            input["green_house"] = GreenHouse.objects.get(id=input.greenhouse)
            del input["greenhouse"]
        except GreenHouse.DoesNotExist:
            raise Exception("Greenhouse with this credentials does not exist.")

        environment = Environment.objects.create(**input)
        environment.save()
        return CreateEnvironment(environment=environment)


class DeleteEnvironment(graphene.Mutation):
    """To delete environment you need to provide 'id'."""

    class Arguments:
        id = graphene.Int(required=True)

    environment = graphene.Field(EnvironmentType)

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        environment = Environment.objects.get(pk=id)
        if info.context.user.is_superuser or info.context.user == environment.green_house.owner:
            environment.delete()
        else:
            raise PermissionDenied
        return None


class EnvironmentMutation(graphene.ObjectType):
    create_environment = CreateEnvironment.Field()
    delete_environment = DeleteEnvironment.Field()


class EnvironmentQuery(graphene.ObjectType):
    environment = graphene.Field(EnvironmentType, id=graphene.Int(required=True))
    environments = graphene.List(EnvironmentType)

    @login_required
    def resolve_environment(root, info, id):
        request_user = info.context.user

        try:
            environment = Environment.objects.get(pk=id)
        except Environment.DoesNotExist:
            raise Exception("Environment with this credentials does not exist.")

        if request_user.is_superuser or request_user == environment.green_house.owner\
                or request_user in environment.green_house.authorized_users:
            return environment
        else:
            raise PermissionDenied

    @login_required
    def resolve_environments(root, info):
        request_user = info.context.user

        if request_user.is_superuser:
            return Environment.objects.all()
        else:
            return Environment.objects.filter(Q(green_house__owner=request_user) |
                                              Q(green_house__authorized_users=request_user))
