import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from greenhouse_management.exceptions import PermissionDenied
from greenhouse_management.graphql.GreenHouse import GreenHouseType
from greenhouse_management.models import *


class DeviceType(DjangoObjectType):
    class Meta:
        model = Device
        fields = '__all__'
    greenhouse = graphene.Field(GreenHouseType)

    def resolve_greenhouse(self, info):
        return self.greenhouse


class FunctionalityEnum(graphene.Enum):
    PASSIVE = 'PA'
    ACTIVE = 'AC'


class DeviceInput(graphene.InputObjectType):
    name = graphene.String()
    functionality = graphene.String()
    greenhouse = graphene.ID()


class CreateDevice(graphene.Mutation):
    """To create device provide 'name', 'functionality' and 'greenhouse'."""

    class Arguments:
        input = DeviceInput(required=True)

    device = graphene.Field(DeviceType)

    @classmethod
    @login_required
    def mutate(cls, root, info, input):
        request_user = info.context.user

        try:         
            if request_user.is_superuser:
                greenhouse = GreenHouse.objects.get(id=input.greenhouse)
            else:
                greenhouse = GreenHouse.objects.get(id=input.greenhouse, owner=request_user)
        except GreenHouse.DoesNotExist:
            raise Exception("Greenhouse with this credentials does not exist.")

        device = Device.objects.create(
            name=input.name,
            functionality=input.functionality,
            greenhouse=greenhouse
        )
        device.save()

        return CreateDevice(device=device)


class UpdateDevice(graphene.Mutation):
    """To update device change 'name', 'functionality' and 'greenhouse'."""

    class Arguments:
        input = DeviceInput(required=True)
        id = graphene.Int(required=True)

    device = graphene.Field(DeviceType)

    @classmethod
    @login_required
    def mutate(cls, root, info, input, id):
        device = Device.objects.get(pk=id)
        if info.context.user.is_superuser or info.context.user == device.greenhouse.owner:
            device.name = input.name if input.name not in ['', None] else device.name
            device.functionality = input.functionality if input.functionality not in ['', None] else device.functionality
            if input.greenhouse:
                try:
                    greenhouse = GreenHouse.objects.get(id=input.greenhouse)
                    if info.context.user.is_superuser or info.context.user == greenhouse.owner:
                        device.greenhouse = greenhouse
                    else:
                        device.greenhouse = device.greenhouse
                        raise Exception("The user is not the owner of the selected greenhouse")
                except GreenHouse.DoesNotExist:
                    raise Exception("Greenhouse with this credentials does not exist.")
            else:
                device.greenhouse = device.greenhouse
            device.save()
        else:
            raise PermissionDenied
        return UpdateDevice(device=device)


class DeleteDevice(graphene.Mutation):
    """To delete device you need to provide 'id'."""

    class Arguments:
        id = graphene.Int(required=True)

    device = graphene.Field(DeviceType)

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        device = Device.objects.get(pk=id)
        if info.context.user.is_superuser or info.context.user == device.greenhouse.owner:
            device.delete()
        else:
            raise PermissionDenied
        return None


class DeviceMutation(graphene.ObjectType):
    create_device = CreateDevice.Field()
    update_device = UpdateDevice.Field()
    delete_device = DeleteDevice.Field()


class DeviceQuery(graphene.ObjectType):
    device = graphene.Field(DeviceType, id=graphene.Int(required=True))
    devices = graphene.List(DeviceType)

    @login_required
    def resolve_device(root, info, id):
        request_user = info.context.user

        try:
            device = Device.objects.get(pk=id)
        except Device.DoesNotExist:
            raise Exception("Device with this credentials does not exist.")

        if request_user.is_superuser or request_user == device.greenhouse.owner:
            return device
        else:
            raise PermissionDenied

    @login_required
    def resolve_devices(root, info):
        request_user = info.context.user

        if request_user.is_superuser:
            return Device.objects.all()
        else:
            return Device.objects.filter(greenhouse__owner=request_user)