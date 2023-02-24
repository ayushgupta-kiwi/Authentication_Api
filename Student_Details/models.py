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

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'Student'


class Political_Leaders(models.Model):
    """
        Create model class to store data in database
    """
    name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=30)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Political Leaders'
