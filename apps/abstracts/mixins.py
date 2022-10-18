#Python
from typing import Any
import random

#Django
from django.core.mail import send_mail

#Rest
from rest_framework.response import Response

#Apps
from abstracts.validators import APIValidator


class ResponseMixin:
    '''ResponseMixin.'''

    def get_json_response(self, data: dict[Any, Any]) -> Response:
        return Response({
            "response": data
        })


class SendEmailMixin:
    """NotificationMixin."""
    def generate_pin(self):
        pin = ''
        for _ in range(5):
            pin += str(random.randint(0, 9))
        return pin

    def send_to_authentifacate(self, pin, user_email: str) -> str:
        try:
            send_mail(
                'Check pin',
                pin,
                'marat.duman@gmail.com',
                [user_email],
                fail_silently=False,
            )
        except Exception as e:
            raise APIValidator(
                f'Ошибка отправки {e}',
                'error',
                '500',
            )