from django.db.models import (
    EmailField,
    CharField,
    ImageField,
    QuerySet,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError


from abstracts.validators import APIValidator
from abstracts.models import AbstractsDateTime


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, login: str, pin: str, password: str) -> 'CustomUser':
        if not email:
            raise ValidationError('Email required')
        try:
            user: 'CustomUser' = self.model(
                email=self.normalize_email(email),
                login=login,
                password=password,
                verificated_code=pin,
            )
            user.set_password(password)
            user.save(using=self._db)
            return user
        except:
            raise APIValidator(
                'Данный пользователь уже существует',
                'message',
                '400',
            )

    def create_superuser(self, email: str, login, pin, password: str) -> 'CustomUser':
        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            login=login,
            verificated_code=pin,
            password=password
        )
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_undeleted_users(self) -> QuerySet['CustomUser']:
        """Get undeleted users"""
        users: QuerySet[CustomUser] = self.filter(deleted_at=None)
        return users


class CustomUser(
    AbstractBaseUser,
    PermissionsMixin,
    AbstractsDateTime
):
    email = EmailField(
        'Почта/Логин',
        unique=True,
        null=False
    )
    login = CharField(
        'Номер телефона',
        unique=True,
        max_length=11, 
        null=True
    )
    verificated_code = CharField('Код подтверждения', max_length=5, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        ordering = (
            'created_at',
        )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'