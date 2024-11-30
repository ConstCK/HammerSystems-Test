from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
import time

from .models import Profile
from .serializers import PhoneNumberSerializer, PassCodeSerializer, ActivateCodeSerializer, ProfileSerializer

from .services import generate_pass_code, generate_invite_code


@api_view(['POST'])
def auth(request):
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
        data = {'phone_number': request.data, 'pass_code': pass_code}
        time.sleep(2)
        return Response(data)
    raise ValidationError('Некорректный номер телефона...')


@api_view(['POST'])
def login(request):
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


@api_view(['POST'])
def activate_code(request):
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


@api_view(['POST'])
def profile(request):
    serializer = PassCodeSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = Profile.objects.filter(pass_code=request.data['pass_code']).first()
        if user:
            data = ProfileSerializer(user, many=False)
            if user.active_invite_code:
                invited_codes_profiles = Profile.objects.filter(active_invite_code=user.invite_code)
                invited_list = [item for item in invited_codes_profiles]
                data = ProfileSerializer({'phone_number': user.phone_number,
                                          'pass_code': user.pass_code,
                                          'invite_code': user.invite_code,
                                          'active_invite_code': user.active_invite_code,
                                          'invited_profiles': invited_list}, many=False)

            return Response({'data': data.data})
        raise ValidationError('Ошибка авторизации...')
