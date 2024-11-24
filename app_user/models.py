from app_user.managers import UserModelManager, CustomerManager, AdminManager
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class UserModel(AbstractUser):
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='Admin/image', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True
    )

    @property
    def full_name(self):
        return f"{self.last_name}, {self.first_name}"

    def __str__(self):
        return self.full_name

class Admin(UserModel):
    objects = AdminManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_customer = False
        self.is_admin = True
        self.is_staff = True
        self.is_superuser = False
        super().save(*args, **kwargs)  # O'z-o'zini chaqirmaslik uchun super ishlatiladi


class Customer(UserModel):
    objects = CustomerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_customer = True
        self.is_admin = False
        self.is_staff = False
        self.is_superuser = False
        super().save(*args, **kwargs)  # O'z-o'zini chaqirmaslik uchun super ishlatiladi
