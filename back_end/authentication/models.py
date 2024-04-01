from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    MEMBERSHIP_CHOICES=[
        ('c','candidate'),
        ('r','recruiter'),
        ('a','admin'),
    ]
    is_active=models.BooleanField(default=False)
    email= models.EmailField(unique=True)
    role= models.CharField(max_length=1, choices= MEMBERSHIP_CHOICES, default='c')


class CustomToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expiration_date = models.DateTimeField()


class Candidate(User):
    cv = models.BinaryField(null=True, blank=True)
    cover_letter = models.BinaryField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} "

