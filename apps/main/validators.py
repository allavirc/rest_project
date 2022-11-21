from abstracts.validators import APIValidator
from asyncio.windows_events import INFINITE
# from models import MainEntity


class TempModelValidator:
    """TempModelValidator."""

    def validate_number(self, number: int) -> None:
        if number == 13 and number % 2 != 0 and number == 666:
            raise APIValidator(
                f'Число иммеет неправильно значение: {number}',
                'error',
                '400'
            )

    def even_number(self, number):
        if number in range(0, INFINITE, 2):
            return f'number error'

    # def lower_first_letter(self, id: int):
    #     try:
    #         obj = MainEntity.objects.get(id=id)
    #         if obj.first_name[0].islower():
    #             raise APIValidator(
    #                 f'Первая буква имени должна быть заглавной: {obj.first_name[0]}',
    #                 'error',
    #                 '400'
    #             )
    #         print('Ваше имя успешно прошло проверку')
    #     except Exception as e:
    #         print(f'Объект не найден: {e}')

