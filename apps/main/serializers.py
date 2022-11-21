from rest_framework.fields import CharField, IntegerField, BooleanField, SerializerMethodField, EmailField, ImageField
from rest_framework.serializers import ModelSerializer
from main.models import MainEntity, Actor, Cartoons


class MainEntitySerializer(ModelSerializer):

    first_name = CharField(required=False, read_only=False)
    last_name = CharField(required=False, read_only=False)
    email = EmailField(required=False, read_only=False)
    phone_number = CharField(required=False, read_only=False)
    apartment_number = IntegerField(required=False, read_only=False)
    has_paid_taxes = BooleanField(required=False, read_only=False)

    class Meta:
        model = MainEntity
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'apartment_number',
            'has_paid_taxes',
        )
#
# class Main2Serializer(ModelSerializer):
#     first_name = CharField(required=False)
#     datetime_created = SerializerMethodField(
#         method_name='get_datetime_created'
#     )
#     datetime_updated = SerializerMethodField(
#         method_name='get_datetime_updated'
#     )
#     datetime_deleted = SerializerMethodField(
#         method_name='get_datetime_deleted'
#     )
#
#
#     class Meta:
#         model = MainEntity
#         fields = (
#             'id',
#             'first_name',
#             'datetime_created',
#             'datetime_updated',
#             'datetime_deleted',
#         )
#
#     def get_datetime_created(self, obj):
#         if '.' in str(obj.datetime_created):
#             return f'{obj.datetime_created}'[:-13]
#         return f'{obj.datetime_created}'[:-9]
#
#     def get_datetime_updated(self, obj):
#         if '.' in str(obj.datetime_updated):
#             return f'{obj.datetime_updated}'[:-13]
#         return f'{obj.datetime_updated}'[:-9]
#
#     def get_datetime_deleted(self, obj: MainEntity) -> str:
#         if not obj.datetime_deleted:
#             return 'Объект не удален'
#
#         if '.' in str(obj.datetime_deleted):
#             return f'{obj.datetime_deleted}'[:-13]
#         return f'{obj.datetime_deleted}'[:-9]


class CartoonSerializers(ModelSerializer):

    name = CharField(required=False)
    released = CharField(required=False)
    img = ImageField(required=False)
    description = CharField(required=False)

    class Meta:
        model = Cartoons
        fields = (
            'id',
            'name',
            'released',
            'img',
            'description',
        )



class ActorsSerializers(ModelSerializer):

    class Meta:
        model = Actor
        fields = '__all__'