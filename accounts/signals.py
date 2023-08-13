from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from .models import User, NotificationModel


@receiver(signal=user_logged_in, sender=User)
def login_welcome_signal(sender, request, user, **kwargs):
    NotificationModel.objects.create(
        body='welcome to our TeamTask',
        to_user=user
    )
