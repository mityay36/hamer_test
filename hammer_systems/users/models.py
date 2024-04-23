import phonenumbers
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField

ROLE_CHOICES = (
    ('user', 'USER'),
    ('moderator', 'MODERATOR'),
    ('admin', 'ADMIN'),
)

REF_CODE_LENGTH = 6
AUTH_CODE_LENGTH = 4
PASSWORD_LENGTH = 18


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        phone_number,
        password='',
        bio='',
        role='user',
        first_name='',
        last_name='',
    ):

        if phone_number is None:
            raise TypeError('Users must have an phone number.')

        user = self.model(
            phone_number=phone_number,
            confirmation_code=self.make_otp(length=AUTH_CODE_LENGTH),
            referral_code=self.make_random_password(length=REF_CODE_LENGTH),
            password=make_password(password),
            role=role,
            bio=bio,
            first_name=first_name,
            last_name=last_name,
        )
        user.save()

        return user

    def create_superuser(
        self,
        phone_number,
        password=None,
        bio='',
        role='admin',
        first_name='',
        last_name='',
    ):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(
            phone_number=phone_number,
            password=password,
            role=role,
            bio=bio,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def make_otp(self, length=4, allowed_chars='123456789'):
        return get_random_string(length, allowed_chars)


class User(AbstractUser):
    username = None
    phone_number = PhoneNumberField(null=False, blank=False, unique=True, region='RU')
    email = models.EmailField(
        unique=True, blank=True, null=True, max_length=128
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=16,
        choices=ROLE_CHOICES,
        default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=AUTH_CODE_LENGTH
    )
    referral_code = models.CharField(
        'Реферальный код пользователя',
        max_length=REF_CODE_LENGTH
    )

    # не совсем уверен по поводу ForeignKey. Вероятно, CharField тоже можно использовать
    user_referrer = models.ForeignKey('self', on_delete=models.SET_NULL,
                                      null=True, blank=True, related_name='referral_received')
    user_referrals = models.ManyToManyField('self', blank=True, related_name='referral_given')

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def __str__(self):
        return self.phone_number.as_e164
