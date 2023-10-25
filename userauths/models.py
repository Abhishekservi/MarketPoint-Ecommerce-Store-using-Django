from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    uid = models.UUIDField(null=True,blank=True)
    email = models.EmailField(unique=True)
    username= models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    USERNAME_FIELD ="email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
        

class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=200)
    subject = models.CharField(max_length=200) 
    message = models.TextField()

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return self.full_name