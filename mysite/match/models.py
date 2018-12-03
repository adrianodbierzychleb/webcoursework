from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField 
#pip install django-multiselectfield


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to='avatars')
    birth_date = models.DateField(null=True, blank=True)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    HOBBY_CHOICES = (
        ('Reading', 'Reading'),
        ('Video games', 'Video games'),
        ('Origami', 'Origami'),
        ('Card games', 'Card games'),
        ('Piano', 'Piano'),
        ('Violin', 'Violin'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    hobbies = models.ManyToManyField(
        to='Hobby',
        blank=True,
        choices= HOBBY_CHOICES,
        symmetrical=False #Not sure if should be False
    ) 
    
#    hobbies = MultiSelectField(choices= HOBBY_CHOICES)
#    my hobbies using multi select 
    
    def __str__(self):
        return self.user.username

class Hobby(models.Model):

    user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.user.name
