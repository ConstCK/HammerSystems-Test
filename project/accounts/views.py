from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
import time

from .models import Profile
from .serializers import PhoneNumberSerializer, PassCodeSerializer, ActivateCodeSerializer, ProfileSerializer, \
    SuccessfulAuthSerializer, SuccessfulLoginSerializer, SuccessResponseSerializer

from .services import generate_pass_code, generate_invite_code


@extend_schema(summary='Authentication',
               request=PhoneNumberSerializer,
               responses={
                   status.HTTP_200_OK: OpenApiResponse(
                       response=SuccessfulAuthSerializer,
                       description='Успешная аутентификация'),
                   status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                       description='Введенные данные некорректны'),
               },
               )
@api_view(['POST'])
def api_auth(request):
    """Представление для api аутентификации пользователя по номеру телефона"""
    serializer = PhoneNumberSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        pass_code = generate_pass_code()
        user = Profile.objects.filter(phone_number=request.data['phone_number']).first()
        if not user:
            Profile.objects.create(phone_number=request.data['phone_number'],
                                   pass_code=pass_code)
        else:
            user.pass_code = pass_code
            user.save()
        data = {'phone_number': request.data['phone_number'], 'pass_code': pass_code}
        time.sleep(2)
        return Response(data)
    raise ValidationError('Некорректный номер телефона...')


@extend_schema(summary='Authorization',
               request=PassCodeSerializer,
               responses={
                   status.HTTP_200_OK: OpenApiResponse(
                       response=SuccessfulLoginSerializer,
                       description='Успешная аутентификация'),
                   status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                       description='Введенные данные некорректны'),
               },
               )
@api_view(['POST'])
def api_login(request):
    """Представление для api авторизации пользователя по 4-значному коду"""
    serializer = PassCodeSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = Profile.objects.filter(pass_code=request.data['pass_code']).first()
        if not user:
            raise ValidationError('Несуществующий pass code...')
        if not user.invite_code:
            invite_code = generate_invite_code()
            user.invite_code = invite_code
            user.save()
        data = {'phone_number': user.phone_number,
                'pass_code': request.data['pass_code'],
                'invite_code': user.invite_code}
        return Response(data)


@extend_schema(summary='Code activation',
               request=ActivateCodeSerializer,
               responses={
                   status.HTTP_200_OK: OpenApiResponse(
                       response=SuccessResponseSerializer,
                       description='Успешная активация кода'),
                   status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                       description='Введенные данные некорректны'),
               },
               )
@api_view(['POST'])
def api_activate_code(request):
    """Представление для api активации 6-значного invite кода"""
    serializer = ActivateCodeSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = Profile.objects.filter(invite_code=request.data['invite_code']).first()
        current_user = Profile.objects.filter(pass_code=request.data['pass_code']).first()
        if not current_user:
            raise ValidationError('Ошибка авторизации...')
        if not user:
            raise ValidationError('Несуществующий invite code...')
        if current_user.active_invite_code:
            raise ValidationError('Вы уже активировали invite code...')

        current_user.active_invite_code = request.data['invite_code']
        current_user.save()

        return Response({'message': 'Invite code успешно активирован'})


@extend_schema(summary='Authorization',
               request=PassCodeSerializer,
               responses={
                   status.HTTP_200_OK: OpenApiResponse(
                       response=ProfileSerializer,
                       description='Получение данных профиля'),
                   status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                       description='Введенные данные некорректны'),
               },
               )
@api_view(['POST'])
def api_profile(request):
    """Представление для api получения данных о текущем пользователе"""
    serializer = PassCodeSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = Profile.objects.filter(pass_code=request.data['pass_code']).first()
        if user:
            data = ProfileSerializer(user, many=False)
            if user.invite_code:
                invited_codes_profiles = Profile.objects.filter(active_invite_code=user.invite_code)
                invited_list = [item for item in invited_codes_profiles]
            else:
                invited_list = []

            data = ProfileSerializer({'phone_number': user.phone_number,
                                      'pass_code': user.pass_code,
                                      'invite_code': user.invite_code,
                                      'active_invite_code': user.active_invite_code,
                                      'invited_profiles': invited_list}, many=False)

            return Response({'data': data.data})
        raise ValidationError('Ошибка авторизации...')


def auth(request):
    """Представление для аутентификации пользователя по номеру телефона"""
    pass


def login(request):
    """Представление для авторизации пользователя по 4-значному коду"""
    pass


def activate_code(request):
    """Представление для активации 6-значного invite кода"""
    pass


def profile(request):
    """Представление для получения данных о текущем пользователе"""
    pass
