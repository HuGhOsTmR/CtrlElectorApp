from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea un perfil automáticamente cuando se crea un usuario solo si no existe."""
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance, ci=0)  # Usa 0 como valor predeterminado para evitar el error

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guarda automáticamente el perfil cuando se guarda el usuario, pero solo si el perfil ya existe."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
