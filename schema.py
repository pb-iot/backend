from greenhouse_management.graphql.User import *


class Mutation(UserMutation, graphene.ObjectType):
    pass


class Query(UserQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
