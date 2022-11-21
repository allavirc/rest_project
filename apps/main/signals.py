# Python
from typing import Any

# Django
from art import tprint
from django.core.mail import send_mail
from django.db.models.base import ModelBase
from django.db.models.signals import (
    post_delete,
    post_save,
    pre_delete,
    pre_save
)
from django.dispatch import receiver

# First party
from main.models import MainEntity


@receiver(
    post_save,
    sender=MainEntity
)
def post_save_tempModel(
    sender: ModelBase,
    instance: MainEntity,
    **kwargs: Any
) -> None:
    """Signal post-save TempModel."""

    first_name = instance.first_name
    apartment_number = instance.apartment_number
    email = instance.email

    tprint('!!! POST_SAVE called !!!')

    # send_mail(
    #     'MainEntity создан | POST_SAVE',
    #     f'Имя {first_name} | Номер квартиры {apartment_number} | Почта {email}',
    #     'allavirc2@gmail.com',
    #     ['allavirc2@gmail.com'],
    #     fail_silently=False,
    # )


@receiver(
    post_save,
    sender=MainEntity
)
def post_save_change_email(
    sender: ModelBase,
    instance: MainEntity,
    **kwargs: Any
) -> None:
    """Signal post-save MainEntity."""

    instance.email = 'error@delete.com'

    print('-----------------------------------------------------------------')
    print('!!! POST_SAVE called !!!')
    print(instance.email)
    print('-----------------------------------------------------------------')



@receiver(
    pre_save,
    sender=MainEntity
)
def pre_save_tempModel(
    sender: ModelBase,
    instance: MainEntity,
    **kwargs: Any
) -> None:
    """Signal post-save TempModel."""

    tprint('!!! PRE_SAVE called !!!')

    # send_mail(
    #     'MainEntity создан | PRE_SAVE',
    #     '. . .',
    #     'allavirc2@gmail.com',
    #     ['allavirc2@gmail.com'],
    #     fail_silently=False,
    # )


@receiver(
    pre_delete,
    sender=MainEntity
)
def pre_delete_tempModel(
    sender: ModelBase,
    instance: MainEntity,
    **kwargs: Any
) -> None:
    """Signal post-save TempModel."""

    first_name = instance.first_name
    apartment_number = instance.apartment_number
    email = instance.email

    tprint('!!! PRE_DELETE called !!!')

    # send_mail(
    #     'MainEntity удаляется | PRE_DELETE',
    #     f'Имя {first_name} | Номер квартиры {apartment_number} | Почта {email}',
    #     'allavirc2@gmail.com',
    #     ['allavirc2@gmail.com'],
    #     fail_silently=False,
    # )


@receiver(
    pre_delete,
    sender=MainEntity
)
def pre_delete_change_email(
    sender: ModelBase,
    instance: MainEntity,
    **kwargs: Any
) -> None:
    """Signal post-save TempModel."""

    instance.email = 'error@delete.com'

    print('-----------------------------------------------------------------')
    print('!!! PRE_DELETE called !!!')
    print(instance.email)
    print('-----------------------------------------------------------------')

