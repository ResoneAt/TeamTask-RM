from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import NotificationModel
from .models import WorkSpaceModel
from accounts.models import User
from .models import WSMembershipModel, BMembershipModel, CMembershipModel


@receiver(signal=post_save, sender=WSMembershipModel)
def add_member_to_workspace_signal(sender, request, instance, **kwargs):
    NotificationModel.objects.create(
        body=f'You have been added to {instance.workspace.title} Workspace'
             f' by {instance.from_user.username}',
        to_user=instance.user
    )


@receiver(post_save, sender=WSMembershipModel)
def send_email_about_add_member_to_workspace_signal(sender, instance, created, **kwargs):
    if created:
        subject = 'TeamTask - You have been added to ...'
        message = (f'You have been added to {instance.workspace.title} Workspace'
                   f' by {instance.from_user.username}'),
        from_email = 'TeamTask.group@gmail.com'
        to_email = instance.to_user.email
        send_mail(subject, message, from_email, [to_email])


@receiver(signal=post_save, sender=BMembershipModel)
def add_member_to_board_signal(sender, request, instance, **kwargs):
    NotificationModel.objects.create(
        body=f'You have been added to {instance.workspace.title} Board '
             f' by {instance.workspace.owner}',
        to_user=instance.user
    )


@receiver(post_save, sender=BMembershipModel)
def send_email_about_add_member_to_board_signal(sender, instance, created, **kwargs):
    if created:
        subject = 'TeamTask - You have been added to ...'
        message = (f'You have been added to {instance.board.title} board'
                   f' by {instance.from_user.username}'),
        from_email = 'TeamTask.group@gmail.com'
        to_email = instance.to_user.email
        send_mail(subject, message, from_email, [to_email])


@receiver(signal=post_save, sender=CMembershipModel)
def assigning_a_card_to_a_member_signal(sender, request, instance, **kwargs):
    NotificationModel.objects.create(
        body=f'A new task has been assigned to you by Ramin as below',
        to_user=instance.user
    )


@receiver(post_save, sender=CMembershipModel)
def send_email_about_add_member_to_card_signal(sender, instance, created, **kwargs):
    if created:
        subject = 'TeamTask - You have been added to ...'
        message = (f'You have been added to {instance.card.title} card'
                   f' by {instance.from_user.username}'),
        from_email = 'TeamTask.group@gmail.com'
        to_email = instance.to_user.email
        send_mail(subject, message, from_email, [to_email])
