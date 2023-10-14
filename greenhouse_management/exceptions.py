from graphql import GraphQLError


class PermissionDenied(GraphQLError):
    def __init__(self):
        super().__init__('You do not have the required permissions to perform this action')
