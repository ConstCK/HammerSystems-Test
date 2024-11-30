from rest_framework import serializers

from .models import Profile


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('phone_number',)

    def is_valid(self, raise_exception=False):
        """Переопределение метода для игнорирования валидации существующих номеров телефона"""

        profile = Profile.objects.filter(phone_number=self.initial_data['phone_number']).first()
        if profile:
            return True
        return super().is_valid(raise_exception=False)


class PassCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('pass_code',)


class ActivateCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('invite_code', 'pass_code')


class ProfileSerializer(serializers.ModelSerializer):
    invited_profiles = PhoneNumberSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ('phone_number', 'pass_code', 'invite_code', 'active_invite_code', 'invited_profiles')
