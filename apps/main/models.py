from datetime import datetime
from typing import Optional, Any

from django.db import models
from django.db.models import Model, QuerySet, Q, F
from abstracts.models import AbstractsDateTime
from .validators import TempModelValidator
from abstracts.services import send
from auths.models import CustomUser


class MainModelQuerySet(QuerySet):
    """MainModelQuerySet"""

    def get_deleted(self) -> QuerySet['MainEntity']: # метод возвращает удаленных
        return self.filter(
            datetime_deleted__isnull=False
        )

    def get_not_deleted(self) -> QuerySet['MainEntity']: # метод возвращает НЕ удаленных
        return self.filter(
            datetime_deleted__isnull=True
        )

    def get_not_updated(self) -> list['MainEntity']:
        objects: QuerySet['MainEntity'] = self.get_not_deleted()
        result = []
        for obj in objects:
            if obj.datetime_updated != obj.datetime_created:
                result.append(obj)
        return result

    def get_obj(self, p_key: str) -> Optional['MainEntity']: # сокращаем try/except во views
        try:
            return self.get(id=p_key)
        except MainEntity.DoesNotExist:
            return None



class MainEntity(AbstractsDateTime, TempModelValidator):
    first_name: str = models.CharField('имя', max_length=255)
    last_name: str = models.CharField('фамилия', max_length=255)
    phone_number: str = models.CharField('номер телефона', max_length=20)
    apartment_number: int = models.IntegerField('номер дома/квартиры')
    has_paid_taxes: bool = models.BooleanField('оплата налогов', default=True)
    email: str = models.EmailField('почта')

    objects = MainModelQuerySet().as_manager()

    class Meta:
        verbose_name = 'Юзер с квартирой'
        verbose_name_plural = 'Юзеры с квартирой'

    def clean(self) -> None:
        # self.validate_number(self.number)
        return super(MainEntity, self).clean()


    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        send(self.email)
        super().save(*args, **kwargs)
        # return super(MainEntity, self).save(*args, **kwargs)

    def delete(self) -> None:
        self.datetime_delete = datetime.now()
        self.save(
            update_fields=['datetime_deleted']
        )

    def __str__(self):
        return f'{self.first_name} -> {self.phone_number}'


class Cartoons(AbstractsDateTime):
    name = models.CharField('название', max_length=255)
    released = models.CharField('дата выпуска', max_length=255)
    img = models.ImageField('афиша', upload_to=None, height_field=None, width_field=None, max_length=100)
    description = models.CharField('описание', max_length=255)

    objects = MainModelQuerySet().as_manager()

    class Meta:
        verbose_name = 'Список Мультфильмов'
        verbose_name_plural = 'Списки Мультфильмов'






class SerialRole(AbstractsDateTime):

    class Choice_type_of_role(models.TextChoices):
        NEGATIVE_CHARACTER = 'Негативный персонаж'
        POSITIVE_CHARACTER = 'Позитивный персонаж'
        NEUTRAL_CHARACTER = 'Нейтральный персонаж'

    name = models.CharField(
        'имя',
        max_length=255,
        unique=True,
        null=False,
    )

    bad_or_good = models.CharField(
        verbose_name='Статус',
        max_length=50,
        choices=Choice_type_of_role.choices,
        default=Choice_type_of_role.NEUTRAL_CHARACTER
    )

    main_person = models.BooleanField(
        'имя',
        default=False
    )

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'



class Actor(AbstractsDateTime):

    first_name = models.CharField('имя', max_length=255, null=False)
    last_name = models.CharField('фамилия', max_length=255, null=False)
    photo_url = models.ImageField('фото', upload_to=None, height_field=None, width_field=None, max_length=100)
    serial_role = models.ForeignKey(SerialRole, max_length=255, null=False, on_delete=models.PROTECT)
    first_appearance_in_serial = models.DateField('Первое появление в сериале', null=False)
    date_birthday = models.DateField('Дата рождения', null=False)

    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'





class Anime(Model):

    studio = models.CharField(
        verbose_name='студия',
        max_length=25,
        null=True
    )
    rating = models.IntegerField(
        verbose_name='рейтинг',
        null=True
    )
    description = models.CharField(
        verbose_name='студия',
        max_length=25,
        null=True
    )
    link = models.CharField(
        verbose_name='ссылка',
        max_length=25,
        null=True
    )
    name = models.CharField(
        verbose_name='название',
        max_length=25,
        null=True
    )
    start_date = models.DateTimeField(
        verbose_name='дата показа',
        null=True
    )

    class Meta:
        verbose_name = 'Аниме'
        verbose_name_plural = 'Много аниме'

    def __str__(self):
        return self.studio


class Genre(Model):

    name = models.CharField(
        verbose_name='студия',
        max_length=25
    )
    anime = models.ManyToManyField(
        Anime,
        related_name='genre',
        verbose_name='аниме'
    )




# class People():
#     def __init__(self, name):
#         self.name = name
#
# people = People() <- instance
#
# self <- instance
# MainModel < - 