from greenhouse_management.graphql.Location import *
from greenhouse_management.graphql.User import *
from greenhouse_management.graphql.Device import *


class Mutation(UserMutation, LocationMutation, DeviceMutation, graphene.ObjectType):
    pass


class Query(UserQuery, LocationQuery, DeviceQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
