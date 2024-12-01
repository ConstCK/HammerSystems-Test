from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, DetailView, UpdateView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
import time

from .forms import AuthForm, LoginForm, ActivateCodeForm
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


class AuthUserView(FormView):
    """Представление для аутентификации пользователя по номеру телефона"""
    form_class = AuthForm
    template_name = 'auth.html'
    extra_context = {'title': 'Аутентификация пользователя по номеру телефона'}

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        pass_code = generate_pass_code()

        try:
            if not form.is_valid():
                return render(request, self.template_name,
                              {'form': form,
                               'title': 'Аутентификация пользователя по номеру телефона'})

            user = Profile.objects.filter(phone_number=form.data['phone_number']).first()
            if not user:
                Profile.objects.create(phone_number=form.cleaned_data['phone_number'],
                                       pass_code=pass_code)
            else:
                user.pass_code = pass_code
                user.save()
            return render(request, 'successful_auth.html',
                          {'pass_code': pass_code})

        except ValidationError:
            form.add_error(None, 'Некорректный номер телефона')
            return render(request, self.template_name, {'form': form,
                                                        'title': 'Аутентификация пользователя по номеру телефона'})


class SuccessfulAuth(TemplateView):
    template_name = 'successful_auth.html'


class LoginView(FormView):
    """Представление для авторизации пользователя по 4-значному коду"""
    form_class = LoginForm
    model = Profile
    template_name = 'login.html'
    # success_url = reverse_lazy('profile')
    extra_context = {'title': 'Авторизация пользователя с использование 4-значного кода'}

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        invite_code = generate_invite_code()

        if form.is_valid():
            user = Profile.objects.filter(pass_code=form.cleaned_data['pass_code']).first()
            if not user:
                form.add_error(None, 'Неверный pass code')
                return render(request, self.template_name,
                              {'form': form,
                               'title': 'Авторизация пользователя с использование 4-значного кода'})
            if not user.invite_code:
                user.invite_code = invite_code
                user.save()
            return redirect(reverse_lazy('profile', kwargs={'pass_code': form.cleaned_data['pass_code']}))
        else:
            form.add_error(None, 'Некорректный pass code')
            return render(request, self.template_name,
                          {'form': form,
                           'title': 'Авторизация пользователя с использование 4-значного кода'})


def activate_code(request):
    """Представление для активации 6-значного invite кода"""
    pass


class ProfileView(FormView):
    """Представление для получения данных о текущем пользователе"""
    model = Profile
    form_class = ActivateCodeForm
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.filter(pass_code=self.kwargs['pass_code']).first()
        invited_profiles = Profile.objects.filter(active_invite_code=profile.invite_code)
        if profile:
            context['profile'] = profile
            context['invited_profiles'] = invited_profiles if invited_profiles else None
            context['title'] = f'Профиль пользователя с номером {profile.phone_number}'
            print('!!', context['invited_profiles'])
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = Profile.objects.filter(invite_code=form.cleaned_data['activated_code']).first()
            current_user = Profile.objects.filter(pass_code = self.kwargs['pass_code']).first()
            if not user:
                form.add_error(None, 'Неверный invite code')
                return render(request, self.template_name,
                              {'form': form,
                               })
            if not current_user.active_invite_code:
                current_user.active_invite_code = form.cleaned_data['activated_code']
                current_user.save()
            return redirect(reverse_lazy('profile', kwargs={'pass_code': self.kwargs['pass_code']}))
        else:
            form.add_error(None, 'Некорректный invite code')
            return render(request, self.template_name,
                          {'form': form}
                           )
