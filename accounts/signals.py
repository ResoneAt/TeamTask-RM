from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from .models import User, NotificationModel


@receiver(signal=user_logged_in, sender=User)
def login_welcome_signal(sender, request, user, **kwargs):
    NotificationModel.objects.create(
        body='welcome to our project',
        to_user=user
    )


@receiver(post_save, sender=User)
def send_email_to_user(sender, instance, created, **kwargs):
    if created:
        subject = 'welcome to TeamTask'
        message = f'Dear {instance.username}, welcome to TeamTask'
        from_email = 'eslamiramin85@gmail.com'
        to_email = instance.email
        send_mail(subject, message, from_email, [to_email])
