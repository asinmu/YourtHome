from django.contrib.auth import get_user_model, authenticate, password_validation
from rest_framework import serializers

from .models import *


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8, write_only=True, required=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'phone', 'name', 'surname']

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            name=validated_data['name'],
            surname=validated_data['surname'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'phone', 'name', 'surname')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError('An username is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        return {
            'username': user.username,
            'token': user.token
        }


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, data):
        if not self.context['request'].user.check_password(data.get('old_password')):
            raise serializers.ValidationError({'old_password': 'Старый паоль введён неправильно. Пожалуйста повторите.'})

        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': 'Не совпадают.'})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user

