from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import MainEntityList, CartoonSet, ActorsSet
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


router: DefaultRouter = DefaultRouter(
    trailing_slash=False # нужно ли ставить слэш в конце (в нашем случае не нужно)
)

router.register(
    'main',
    MainEntityList,
)
router.register(
    'main2',
    CartoonSet,
)
router.register(
    'main3',
    ActorsSet,
)

# router.register(
#     'main2',
#     MainEntity2
# )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]


urlpatterns += [
    path(
        'api/v1/',
        include(router.urls)
    ),
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
]