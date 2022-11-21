from datetime import datetime
from typing import Any, Optional, Union
from django.db.models import QuerySet
from django.http import HttpResponse
from rest_framework.response import Response
from abstracts.validators import APIValidator
from django.core.mail import send_mail, EmailMessage
import sendsms


# будет обрабатывать ответ (Respons)
from abstracts.paginators import (
    AbstractPageNumberPaginator,
    AbstractLimitOffsetPaginator
)


class ResponseMixin:
    """ResponceMixin."""

    def get_json_response(
        self,
        data: dict[Any, Any],
        paginator: Optional[
            Union[
                AbstractPageNumberPaginator,
                AbstractLimitOffsetPaginator
            ]
        ] = None
    ) -> Response:

        if paginator:
            return paginator.get_paginated_response(
                data
            )
        return Response(
            {
                'results': data
            }
        )

class ValidationMixin:
    """ValidationMixin"""

    def get_obj_if_exists_raise_if_doesnt(
            self,
            queryset: QuerySet[Any],
            p_key: str
    ) -> None:

        obj: Any = queryset.get_obj(
            p_key
        )
        if not obj:
            raise APIValidator(
                f'Объект не найден {p_key}',
                'error',
                '404'
            )
        return obj


    def allow_delete_only_is_activated(
            self,
            queryset: QuerySet[Any],
            p_key: str
    ) -> Optional[tuple]:

        obj: Any = queryset.get_obj(
            p_key
        )

        if not obj:
            raise APIValidator(
                f'Объект не найден {p_key}',
                'error',
                '404'
            )

        if obj.is_activated:

            # obj.datetime_deleted = datetime.now()

            obj.delete()

            return (f'Объект удален: {obj.datetime_deleted}')

        return (f'Объект уже был удален {obj.datetime_deleted}')


    def raise_if_tempmodel_violates_create_restrictions(self, number: int):

        if number % 2 == 1:
            raise APIValidator(
                f'Это число не может быть четным {number}',
                'error',
                '404'
            )
        return number


class NotificationMixin:
    """NotificationMixin"""
    def send_email(
            self,
            user_email: str):
        try:
            EmailMessage(
                'Hello',
                'Body goes here',
                'from@example.com',
                [user_email],
                reply_to=['another@example.com'],
                headers={'Message-ID': 'foo'},
            )

        except Exception as e:
            raise f'Почта не найдена: {e}'

        return f'Сообщение отправлено на почту: {user_email}'


    def send_message(self, user_phone_number: str) -> HttpResponse:

        try:
            api.send_sms(
                body='I can haz txt', from_phone='+77019500000', to=[user_phone_number]
            )
        except Exception as e:
            raise f'Телефон не найден: {e}'

        for sms in sendsms.outbox:
            print(sms.from_phone)
            print(sms.to)
            print(sms.body)

        return HttpResponse('Message send')
