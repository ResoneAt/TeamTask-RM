from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import NotificationModel
from .models import WorkSpaceModel
from accounts.models import User



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


# @receiver(post_save, sender=User)
# def add_member_to_workspace(sender, instance, created, **kwargs):
#     if created:
#         workspace = WorkSpaceModel.objects.get()
            # isinstance.member.add(workspace)