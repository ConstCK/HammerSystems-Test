from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    invited_list = serializers.ListSerializer(read_only=True)

    class Meta:
        fields = ('phone_number', 'pass_code', 'invite_code', 'active_invite_code', 'invited_list')
