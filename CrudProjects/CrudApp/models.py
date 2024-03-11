from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

GENDER_CHOICES = (
    ('male','MALE'),
    ('female', 'FEMALE'),
    ('others', 'OTHERS'),
)

class UserField(AbstractUser):
    birth_date =  models.DateField(null=True, blank=True)
    user_gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    user_designation = models.CharField(max_length=100)
    is_manager = models.BooleanField(default=True)
    is_employee = models.BooleanField(default=False)
    images = models.ImageField(upload_to='pictures')