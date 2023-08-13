from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import NotificationModel


@receiver(signal=post_save, sender='WSMembershipModel')
def add_to_workspace_signal(sender, request, instance, **kwargs):
    NotificationModel.objects.create(
        body=f'You have been added to Workspace {instance.workspace.title}'
             f' by {instance.workspace.owner}',
        to_user=instance.user
    )


@receiver(signal=post_save, sender='BMembershipModel')
def add_to_board_signal():
    ...