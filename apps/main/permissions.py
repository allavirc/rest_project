from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class TempPermissions(BasePermission):
    """TempPermissions."""

    def __init__(self) -> None:
        self._admin: bool = False
        self._user: bool = False

    def _init_permissions(self, request: Request) -> None:

        self._user = (
            request.user and
            request.user.is_active
        )
        self._admin = self._user and (
            request.user.is_staff and
            request.user.is_superuser
        )

    def has_permission(self, request: Request, view: 'TempViewSet') -> bool:

        self._init_permissions(request)

        basic_endpoints: list[str] = [
            'list',
            'list-2',
            'retrieve'
        ]
        advanced_endpoints: list[str] = [
            'create',
            'partial_update',
            'update',
            'destroy'
        ]
        if view.action in basic_endpoints:
            return self._user

        if view.action in advanced_endpoints:
            return self._admin

        return False
