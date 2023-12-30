from graphene_django import DjangoObjectType
from greenhouse_management.models import *


class GreenHouseType(DjangoObjectType):
    class Meta:
        model = GreenHouse
        fields = '__all__'
