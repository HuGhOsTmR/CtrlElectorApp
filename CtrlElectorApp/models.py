from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ci = models.IntegerField(unique=True)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    is_verified = models.BooleanField(default=False) 
    id_front = models.ImageField(upload_to="verifications/", null=True, blank=True)  # Anverso del CI
    id_back = models.ImageField(upload_to="verifications/", null=True, blank=True)   # Reverso del CI
    selfie_with_id = models.ImageField(upload_to="verifications/", null=True, blank=True)  # Selfie con CI

    def __str__(self):
        return self.user.username
