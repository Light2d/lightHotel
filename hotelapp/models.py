from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission

class Gender(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'

class Role(models.TextChoices):
    USER = 'user', 'User'
    CLIENT = 'client', 'Client'
    ADMIN = 'admin', 'Admin'

class CustomUser(AbstractUser):
    patronymic = models.CharField(max_length=64, null=True, blank=True)
    phone_number = models.CharField(max_length=12, unique=True)
    registration_address = models.TextField()
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.MALE)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    is_banned = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'phone_number', 'registration_address', 'gender', 'role']

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Уникальное имя для обратной связи
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Уникальное имя для обратной связи
        blank=True
    )


class HotelRoom(models.Model):
    class RoomCategory(models.TextChoices):
        SINGLE_STANDARD = 'single_standard', 'Одноместный стандарт'
        TRIPLE_BUDGET = 'triple_budget', 'Трехместный бюджет'

    class RoomStatus(models.TextChoices):
        FREE = 'free', 'Free'
        BUSY = 'busy', 'Busy'
        CLEANING = 'cleaning', 'Cleaning'

    name = models.CharField(max_length=32)
    description = models.TextField()
    category = models.CharField(max_length=32, choices=RoomCategory.choices)
    status = models.CharField(max_length=32, choices=RoomStatus.choices, default=RoomStatus.FREE)
    price = models.FloatField()
