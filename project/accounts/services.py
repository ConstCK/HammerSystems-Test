import string
import random

from rest_framework.exceptions import ValidationError


def generate_pass_code() -> str:
    while True:
        code = list(string.digits)
        result = (random.choices(code, k=4))
        return ''.join(result)


def generate_invite_code() -> str:
    while True:
        code = list(string.digits + string.ascii_letters)
        result = random.choices(code, k=6)
        return ''.join(result)


def phone_number_validator(number: str) -> None:
    try:
        num = int(number[1:])
        print(num)
        if len(number) != 12 or not number.startswith('+') or not str(num).isdigit():
            raise ValidationError('Некорректный номер телефона')
    except:
        raise ValidationError('Некорректный номер телефона')

def pass_code_validator(number: str) -> None:
    try:
        num = int(number)
    except:
        raise ValidationError('Некорректный pass code')
