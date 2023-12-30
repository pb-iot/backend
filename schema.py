from greenhouse_management.graphql.User import *
from greenhouse_management.graphql.Device import *


class Mutation(UserMutation, DeviceMutation, graphene.ObjectType):
    pass


class Query(UserQuery, DeviceQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
