from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User, REF_CODE_LENGTH
from core.utils import send_otp_code


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    confirmation_code = serializers.CharField(max_length=12, read_only=True)

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'confirmation_code')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        # имитация отправки 4-х значного кода
        send_otp_code()

        return {
            'phone_number': user.phone_number,
            'confirmation_code': user.confirmation_code,
        }


class TokenSerializer(serializers.ModelSerializer, TokenObtainPairSerializer):

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'confirmation_code')

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        confirm_code = None
        if 'request' in self.context:
            authenticate_kwargs['request'] = self.context['request']
            confirm_code = self.context['request'].data['confirmation_code']

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None:
            raise NotFound(
                'User does not exist.'
            )

        if self.user.confirmation_code != confirm_code:
            raise serializers.ValidationError(
                'Invalid confirmation_code.'
            )

        access = AccessToken.for_user(self.user)

        return {
            'token': str(access)
        }


class UserSerializer(serializers.ModelSerializer):
    user_referrer = serializers.CharField(max_length=REF_CODE_LENGTH, write_only=True)

    class Meta:
        model = User
        fields = (
            'phone_number', 'first_name', 'last_name',
            'bio', 'role', 'user_referrer', 'referral_code', 'user_referrals'

        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return {
            'phone_number': user.phone_number,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': user.bio,
            'role': user.role,
        }

    def update(self, instance, validated_data):
        referral_code = self.context['request'].data['user_referrer']
        if referral_code:
            referrer = User.objects.get(referral_code=referral_code)
            instance.user_referrer = referrer
            instance.save()
            referrer.user_referrals.add(instance)
            return instance
        else:
            return super().update(instance, validated_data)
