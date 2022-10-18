from django.db.models import QuerySet

# Rest
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request

# Apps
from abstracts.mixins import ResponseMixin, SendEmailMixin
from auths.serializers import UserSerializer
from auths.models import CustomUser


class UserViewSet(
    SendEmailMixin,
    ResponseMixin,
    ViewSet,
    RetrieveAPIView,
):
    queryset: QuerySet[CustomUser] = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(
        methods=['post'],
        detail=False,
        url_path='create-account',
        permission_classes=(
            AllowAny,
        )
    )
    def create_account(self, request: Request):
        login = request.data['login']
        email = request.data['email']
        password = 'qwerty'
        pin = self.generate_pin()
        CustomUser.objects.create_user(
            email, login, pin, password
        )
        return Response(status=201)

    @action(
        methods=['post'],
        detail=False,
        url_path='set-password',
        permission_classes=(
            AllowAny,
        )
    )
    def set_password(self, request):
        email = request.data['email']
        password = request.data['password']
        pin = request.data['pin']
        try:
            user: CustomUser = CustomUser.objects.get(
                email=email
            )
        except:
            return Response(data={'message': 'Такой пользователь не найден'}, status=404)
        if not user.verificated_code:
            return Response(data={'message': 'Вы авторизованы'}, status=500)
        elif user.verificated_code != pin:
            return Response(data={'message': 'Неверный пин код'}, status=500)
        user.verificated_code = None
        user.set_password(password)
        user.save()
        return Response(status=201)

    def retrieve(self, request, pk):
        try:
            serializer: UserSerializer = \
                UserSerializer(
                    self.queryset.get(id=pk)
                )
        except:
            return Response(
                data={'message': 'Такой пользователь не найден'},
                status=404
            )
        return Response(
            data=serializer.data,
            status=201
        )
