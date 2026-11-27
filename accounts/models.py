from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("farmer", "Farmer"),
        ("buyer", "Buyer"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="buyer")
    email = models.EmailField(blank=True)
    username = models.CharField(max_length=150, unique=True)
    middle_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True, null=True)
    crops_grown = models.TextField(blank=True, null=True)
    favorite_crops = models.TextField(blank=True, null=True)
    farm_size = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", default="default-pics.png", blank=True, null=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return f"Profile: {self.user.username}"
