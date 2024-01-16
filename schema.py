from greenhouse_management.graphql.Location import *
from greenhouse_management.graphql.User import *
from greenhouse_management.graphql.Device import *
from greenhouse_management.graphql.Enviroment import *


class Mutation(UserMutation, LocationMutation, DeviceMutation, EnvironmentMutation, graphene.ObjectType):
    pass


class Query(UserQuery, LocationQuery, DeviceQuery, EnvironmentQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
