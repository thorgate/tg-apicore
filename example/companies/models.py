from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    created = models.DateTimeField(auto_now_add=True, editable=False)


class Company(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)


class Employment(models.Model):
    ROLE_NORMAL = 1
    ROLE_MANAGER = 2

    ROLE_CHOICES = (
        (ROLE_NORMAL, 'normal'),
        (ROLE_MANAGER, 'manager'),
    )

    user = models.ForeignKey(User, related_name='employments', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=ROLE_NORMAL)
    created = models.DateTimeField(auto_now_add=True, editable=False)
