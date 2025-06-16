from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Este é o nosso modelo de Perfil. 
# Ele terá uma relação de um-para-um com o User do Django.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_technician = models.BooleanField('É técnico', default=False)

    def __str__(self):
        return self.user.username

# Estes "signals" garantem que um Perfil seja criado ou salvo
# automaticamente sempre que um User for criado ou salvo.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()