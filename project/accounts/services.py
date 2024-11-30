import string
import random

from rest_framework.exceptions import ValidationError


def generate_pass_code() -> int:
    digits = list(string.digits)
    return int(''.join(random.choices(digits, k=4)))


def generate_invite_code() -> str:
    digits = list(string.digits + string.ascii_letters)
    return ''.join(random.choices(digits, k=6))


def phone_number_validator(number: str) -> None:
    if len(number) != 12 or not number.startswith('+'):
        raise ValidationError('Некорректный номер телефона')
