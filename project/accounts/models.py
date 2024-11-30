from django.db import models

from accounts.services import phone_number_validator


class Profile(models.Model):
    phone_number = models.CharField(max_length=12, unique=True, verbose_name='Номер телефона',
                                    help_text='Номер телефона в формате +79181234567',
                                    validators=[phone_number_validator])
    pass_code = models.CharField(max_length=4, null=True, blank=True,
                                 verbose_name='4-значный код для входа')
    invite_code = models.CharField(null=True, blank=True,
                                   verbose_name='6-значный код-приглашение')
    active_invite_code = models.CharField(null=True, blank=True,
                                          verbose_name='активированный 6-значный код-приглашение')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['phone_number']
