from greenhouse_management.graphql.Location import *
from greenhouse_management.graphql.User import *
from greenhouse_management.graphql.Device import *
from greenhouse_management.graphql.Enviroment import *
from greenhouse_management.graphql.GreenHouse import *


class Mutation(UserMutation, LocationMutation, DeviceMutation, GreenHouseMutation, EnvironmentMutation, graphene.ObjectType):
    pass


class Query(UserQuery, LocationQuery, DeviceQuery, EnvironmentQuery, GreenHouseQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
