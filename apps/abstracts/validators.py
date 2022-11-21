from typing import Optional

from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.exceptions import APIException

from django.core.exceptions import ValidationError


class APIValidator(APIException):
    """General-purpose validator for API."""

    status_code: Optional[int] = None
    status_map: dict[str, int] = {
        '500': HTTP_500_INTERNAL_SERVER_ERROR,
        '404': HTTP_404_NOT_FOUND,
        '403': HTTP_403_FORBIDDEN,
        '400': HTTP_400_BAD_REQUEST,
    }

    def __init__(
        self, message: str, field: str, code: str = '400'
    ) -> None:

        self.status_code = self.status_map.get(
            code, None
        )
        if not self.status_code:
            raise ValidationError(
                'Статус код неизвестен'
            )

        if message:
            self.detail = {
                field: message
            }
        else:
            self.detail = {
                'error': 'Сервер не отвечает'
            }