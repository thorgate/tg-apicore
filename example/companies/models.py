from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    pass


class Company(BaseModel):
    reg_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=64)
    email = models.EmailField(blank=True)


class Employment(BaseModel):
    ROLE_NORMAL = 1
    ROLE_ADMIN = 2

    ROLE_CHOICES = (
        (ROLE_NORMAL, 'normal'),
        (ROLE_ADMIN, 'admin'),
    )

    user = models.ForeignKey(User, related_name='employments', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=ROLE_NORMAL)

    class Meta:
        unique_together = (('user', 'company'),)
