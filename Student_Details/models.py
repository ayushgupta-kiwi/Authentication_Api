from django.db import models

from django.contrib.auth.models import AbstractUser


class Student_Info(AbstractUser):
    """
        Define a new model that extends Django's AbstractUser model
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=255, unique=True)
    contact = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'Student'

    def __str__(self):
        return self.username

