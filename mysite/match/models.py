from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Hobby(models.Model):

    name = models.TextField()

    def __str__(self):
        return self.name


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(default="default.jpg", upload_to='avatars')
    birth_date = models.DateField(null=True)

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    hobbies = models.ManyToManyField(Hobby, blank=True)

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.user.username
