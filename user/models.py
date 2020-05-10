from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, name, surname, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(
            name=name,
            surname=surname,
            phone=phone,
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        if username is None:
            raise TypeError('Users must have a email.')
        if password is None:
            raise TypeError('Superusers must have a password.')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Логин', db_index=True, max_length=30, unique=True,
                                error_messages={
                                    'unique': "A user with that username already exists."
                                }
                                )
    email = models.EmailField('Адрес электронной почты', db_index=True)
    name = models.CharField('Имя', max_length=100, blank=True)
    surname = models.CharField('Фамилия', max_length=100, blank=True)
    phone = models.CharField('Номер телефона', max_length=100, blank=True)
    is_active = models.BooleanField('Статус', default=True)
    is_staff = models.BooleanField('Персонал', default=False)
    date_of_add = models.DateTimeField('Дата регистрации', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'surname', 'email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return f'{self.username}'

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
