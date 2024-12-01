from rest_framework import serializers

from .models import Profile


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('phone_number',)


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


class SuccessfulAuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    pass_code = serializers.CharField()


class SuccessfulLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    pass_code = serializers.CharField()
    invite_code = serializers.CharField()


class SuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
