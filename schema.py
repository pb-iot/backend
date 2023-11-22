from greenhouse_management.graphql.Location import *
from greenhouse_management.graphql.User import *


class Mutation(UserMutation, LocationMutation, graphene.ObjectType):
    pass


class Query(UserQuery, LocationQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
