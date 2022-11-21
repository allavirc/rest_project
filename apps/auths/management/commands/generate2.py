import random
import names
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from main.models import MainEntity


class Command(BaseCommand):
    """Custom command for filling up database

    Test data only
    """
    help = "Custom command for genarate data for filling up database"

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        pass

    def _generate_number(self) -> int:
        """Generate number"""

        _number_from: int = 10
        _number_to: int = 99

        return random.randint(
            _number_from,
            _number_to
        )

    def _generate_user(self) -> None:
        """Generate user/customuser objects"""

        TOTAL_USER_COUNT = 500

        first_name = names.get_first_name()
        last_name = names.get_last_name()


        def generate_email() -> str:
            _email_patterns: tuple = (
                'gmail.com', 'mail.ru',
                'yandex.ru', 'mail.ua',
                'inbox.ua', 'yahoo.com',
                'bk.ru', 'yandex.kz',
            )
            return '{0}_{1}@{2}'.format(
                first_name.lower(),
                last_name.lower(),
                random.choice(_email_patterns)
            )

        def generate_first_name():
            first_name = names.get_first_name()
            return first_name

        def generate_last_name():
            last_name = names.get_last_name()
            return last_name

        def generate_phone_number():
            phone: str = '+7-'
            first_nums: str = ''
            sec_nums: str = ''
            third_nums: str = ''
            fifth_nums: str = ''

            for i in range(3):
                first_nums += str(random.randint(1, 9))
            for i in range(3):
                sec_nums += str(random.randint(1, 9))
            for i in range(2):
                third_nums += str(random.randint(1, 9))
            for i in range(2):
                fifth_nums += str(random.randint(1, 9))

            return phone + '{0}-{1}-{2}-{3}'.format(
                first_nums,
                sec_nums,
                third_nums,
                fifth_nums
            )

        def generate_apartment_number():
            return random.randint(1, 100)

        def generate_has_paid_taxes():
            choice: list = [True, False]
            return random.choice(choice)

        # User fields
        email: str = ''
        password: str = ''

        _: int

        for _ in range(TOTAL_USER_COUNT):
            first_name = generate_first_name()
            last_name = generate_last_name()
            phone_number = generate_phone_number()
            apartment_number = generate_apartment_number()
            has_paid_taxes = generate_has_paid_taxes()
            email = generate_email()

            user: dict = {
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'apartment_number': apartment_number,
                'has_paid_taxes': has_paid_taxes,
                'email': email,
            }
            try:
                MainEntity.objects.get(email=email)
            except MainEntity.DoesNotExist:
                continue

            MainEntity.objects.get_or_create(**user)

    def handle(self, *args, **kwargs):
        """Handles data filling"""

        start: datetime = datetime.now()

        self._generate_user()

        print(
            'Generating Data: {} seconds'.format(
                (datetime.now()-start).total_seconds()
            )
        )
