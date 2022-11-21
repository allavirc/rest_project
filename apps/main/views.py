from datetime import datetime
from typing import Optional, Any, Type

from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.db.models import QuerySet

from main.models import MainEntity, Cartoons, Actor
from main.serializers import MainEntitySerializer, CartoonSerializers, ActorsSerializers

from abstracts.mixins import ResponseMixin, ValidationMixin, NotificationMixin
from abstracts.paginators import AbstractPageNumberPaginator

from main.permissions import TempPermissions


class MainEntityList(
    ResponseMixin,
    ValidationMixin,
    ViewSet
):
    """TempViewSet."""

    permission_classes = (
        TempPermissions,
    )

    queryset: QuerySet[MainEntity] = MainEntity.objects.all()
    # queryset: QuerySet[MainEntity] = MainEntity.objects.filter(datetime_deleted__isnull=True)

    pagination_class: Type[AbstractPageNumberPaginator] = \
        AbstractPageNumberPaginator

    def retrieve(self, request: Request, pk: str) -> Response:

        obj: Optional[MainEntity] = None

        try:
            obj = self.queryset.get(
                id=pk
            )
        except MainEntity.DoesNotExist:
            return self.get_json_response(
                {
                    'message': 'Объект не найден',
                    'payload': {
                        'invalid_obj_id': f'{pk}'
                    }
                }
            )

        serializer: MainEntitySerializer = MainEntitySerializer(obj)

        return self.get_json_response(
            serializer.data
        )

    # @action(
    #     methods=['get'],
    #     detail=False,
    #     url_path='list-2',
    #     permission_classes=(
    #             AllowAny,
    #     )
    # )
    # def list_2(self, request: Request) -> Response:
    #     serializer: Main2Serializer = \
    #         Main2Serializer(
    #             self.queryset,
    #             many=True
    #         )
    #
    #     return self.get_json_response(serializer.data) # обработчик в mixins
    #     # return Response(
    #     #     serializer.data
    #     # )



    def list(self, request):
        # serializer: MainEntitySerializer = MainEntitySerializer(self.queryset.get_not_deleted(), many=True)
        # get_not_deleted метод из MainModelQuerySet(менеджера)
        # чтобы не прописывать get или filter прописали готовую функцию

        paginator: AbstractPageNumberPaginator = \
            self.pagination_class()

        objects: list[Any] = paginator.paginate_queryset(
            self.queryset,
            request
        )
        serializer: MainEntitySerializer = \
            MainEntitySerializer(
                objects,
                many=True
            )
        return self.get_json_response(
            serializer.data,
            paginator
        )

    def create(self, request: Request) -> Response:

        serializer: MainEntitySerializer = MainEntitySerializer(data=request.data)

        if not serializer.is_valid():
            return self.get_json_response(
                {
                    'message': 'Объект не был создан',
                    'payload': request.data
                }
            )

        serializer.save()
        return self.get_json_response(
            {
                'message': 'Объект был создан',
            }
        )

    def update(self, request: Request, pk: str) -> Response:

        obj: MainEntity = self.get_obj_or_raise(
            self.queryset,
            pk
        )
        serializer: MainEntitySerializer = \
            MainEntitySerializer(
                obj,
                data=request.data
            )
        request.data['obj_id'] = obj.id

        if not serializer.is_valid():
            return self.get_json_response(
                {
                    'message': 'Объект не был обновлен',
                    'payload': request.data
                }
            )

        serializer.save()

        return self.get_json_response(
            {
                'message': 'Объект был обновлен',
                'payload': request.data
            }
        )

    def partial_update(self, request: Request, pk: str) -> Response:

        obj: MainEntity = self.get_obj_if_exists_raise_if_doesnt(
            self.queryset,
            pk
        )
        serializer: MainEntitySerializer = \
            MainEntitySerializer(
                obj,
                data=request.data,
                partial=True
            )
        request.data['obj_id'] = obj.id

        if not serializer.is_valid():
            return self.get_json_response(
                {
                    'message': 'Объект не был частично-обновлен',
                    'payload': request.data
                }
            )

        serializer.save()

        return self.get_json_response(
            {
                'message': 'Объект был частично-обновлен',
                'payload': request.data
            }
        )

    def delete_for(self, request, pk):
        object: MainEntity = self.queryset.get(id=pk)

        object.delete()

        return object

    def destroy(self, request, pk):

        object: MainEntity = self.delete_for(request, pk)

        return self.get_json_response(
            {
                'obj id': f'{object.id}',
                'message': 'Объект был удален',
                'object_daleted': f'{object.datetime_deleted}'
             }
        )

    def send_email(self, user_email):

        self.send_email(user_email)



#
# class MainEntity2(ViewSet):
#     """MainEntity2"""
#
#     queryset: QuerySet[MainEntity] = MainEntity.objects.all()
#
#     def list(self, request):
#         serializer: MainEntitySerializer = \
#             MainEntitySerializer(
#                 self.queryset.get_not_updated(),
#                 many=True
#             )
#
#         return Response(serializer.data)
#
#
#     def custom_delete(self, request, pk):
#         try:
#             obj: MainEntity = self.queryset.get(id=pk)
#         except Exception as e:
#             return f'Not active objects {e}'
#
#         obj.delete()
#
#         return obj
#
#
#     def destroy(self, request: Request, pk: str) -> Response:
#
#         obj: MainEntity = self.custom_delete(request, pk)
#
#         return Response(
#             {
#                 'obj id': f'ID: {obj.id}',
#                 'message': f'Объект {obj.first_name} {obj.last_name} {obj.id} был удален',
#                 'object_daleted': f'Время удаления: {obj.datetime_deleted}'
#             }
#         )
#
#

class CartoonSet(ViewSet):
    queryset: QuerySet[Cartoons] = Cartoons.objects.all()

    def list(self, request):
        serializer: ActorsSerializers = \
            ActorsSerializers(
                self.get_not_updated(),
                many=True
            )

        return Response(serializer.data)


    def retrieve(self, request: Request, pk: str) -> Response:

        obj: Optional[Cartoons] = Cartoons.objects.get(id=pk)
        serializer: CartoonSerializers = CartoonSerializers(obj)
        try:
            obj = self.queryset.get(
                id=pk
            )
        except Cartoons.DoesNotExist:
            return self.get_json_response(
                {
                    'message': 'Объект не найден',
                    'payload': {
                        'invalid_obj_id': f'{pk}'
                    }
                }
            )

        return self.get_json_response(
            serializer.data
        )

    def update(self, request: Request, pk: str) -> Response:

        obj: Cartoons = self.get_obj_or_raise(
            self.queryset,
            pk
        )
        serializer: CartoonSerializers = \
            CartoonSerializers(
                obj,
                data=request.data
            )
        request.data['obj_id'] = obj.id

        if not serializer.is_valid():
            return self.get_json_response(
                {
                    'message': 'Объект не был обновлен',
                    'payload': request.data
                }
            )

        serializer.save()

        return self.get_json_response(
            {
                'message': 'Объект был обновлен',
                'payload': request.data
            }
        )



class ActorsSet(ViewSet):

    queryset: QuerySet[Actor] = Actor.objects.all()

    def list(self, request):
        serializer: ActorsSerializers = \
            ActorsSerializers(
                self.queryset,
                many=True
            )

        return Response(serializer.data)

    def retrieve(self, request: Request, pk: str) -> Response:

        obj: Optional[Actor] = Actor.objects.get(id=pk)
        serializer: ActorsSerializers = ActorsSerializers(obj)
        try:
            obj = self.queryset.get(
                id=pk
            )
        except Cartoons.DoesNotExist:
            return self.get_json_response(
                {
                    'message': 'Объект не найден',
                    'payload': {
                        'invalid_obj_id': f'{pk}'
                    }
                }
            )

        return self.get_json_response(
            serializer.data
        )

    def create(self, request: Request) -> Response:

        serializer: ActorsSerializers = ActorsSerializers(data=request.data)

        if not serializer.is_valid():
            return self.get_json_response(
                {
                    'message': 'Объект не был создан',
                    'payload': request.data
                }
            )

        serializer.save()
        return self.get_json_response(
            {
                'message': 'Объект был создан',
            }
        )

    def delete(self, request, pk):
        try:
            obj: MainEntity = self.queryset.get(id=pk)
        except Exception as e:
            return f'Not active objects {e}'

        obj.delete()

        return obj


