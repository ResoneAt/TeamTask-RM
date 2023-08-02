from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.shortcuts import reverse
from core.models import BaseModel, SoftDeleteModel
from .manager import MyUserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, BaseModel, SoftDeleteModel):
    username = models.CharField(verbose_name=_('Username'),
                                max_length=250, unique=True,
                                null=False, blank=False,
                                help_text=_('Please enter your username'))
    email = models.EmailField(verbose_name=_('Email'),
                              unique=True,
                              null=False, blank=False,
                              help_text=_('Please enter your email'))
    full_name = models.CharField(verbose_name=_('Full name'),
                                 max_length=250,
                                 null=True, blank=True,
                                 help_text=_('Please enter your full name'))
    bio = models.TextField(verbose_name=_('Bio'),
                           null=True, blank=True,
                           help_text=_('Please write about yourself'))
    image = models.ImageField(verbose_name=_('Image'),
                              upload_to='user',
                              null=True, blank=True,
                              help_text=_('Please upload your image.'))

    job_title = models.CharField(verbose_name=_('Job title'),
                                 max_length=250,
                                 null=True, blank=True,
                                 help_text=_('Please enter your job title'))
    developer = 1
    digital_marketing = 2
    business = 3
    education = 4
    personal_planning = 5
    work_field_choices = ((developer, 'Developer'),
                          (digital_marketing, 'Digital marketing'),
                          (business, 'Business'),
                          (education, 'Education'),
                          (personal_planning, 'Personal_planning'))
    work_field = models.IntegerField(verbose_name=_('Work field'),
                                     choices=work_field_choices,
                                     null=True, blank=True,
                                     help_text=_('Please enter your work field'))

    is_admin = models.BooleanField(verbose_name=_('Is Admin'),
                                   default=False)

    updated_at = models.DateTimeField(verbose_name=_('Updated at'),
                                      auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [username]

    objects = MyUserManager()

    class Meta:
        verbose_name, verbose_name_plural = _('User'), _('Users')
        db_table = 'User'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def seen_pv_message(self, from_user):
        messages = PvMessageModel.objects.filter(from_user=from_user,
                                                 to_user=self,
                                                 is_read=False)
        messages.update(is_read=True)

    def add_to_work_space(self):
        ...

    def add_to_board(self):
        ...

    def add_to_card(self):
        ...

    def delete_from_work_space(self):
        ...

    def delete_from_board(self):
        ...

    def delete_from_card(self):
        ...

    def get_absolut_url(self):
        kwargs = {
            'user_id': self.pk
        }
        return reverse('accounts:user_profile', kwargs=kwargs)

    def __str__(self):
        return self.email


class GMessageModel(BaseModel, SoftDeleteModel):
    from_user = models.ForeignKey(User,
                                  on_delete=models.DO_NOTHING,
                                  related_name='sender')
    text = models.TextField(help_text='Please Write Your Message')
    board = models.ForeignKey('BoardModel',
                              on_delete=models.DO_NOTHING)
    
    class Meta:
        verbose_name, verbose_name_plural = _("GMessage"), _("GMessages")
        db_table = 'GroupMessage'
    
    def send_message(self):
        pass

    def seen_message(self):
        pass
    
    def __str__(self) -> str:
        return f'{self.from_user} : {self.text}'


class PvMessageModel(BaseModel, SoftDeleteModel):
    from_user = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                  related_name='sender')
    to_user = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                related_name='receiver')
    text = models.TextField(help_text='Please Write Your Message')
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name, verbose_name_plural = _("Message"), _("Messages")
        db_table = 'PrivateMessage'

    def send_message(self):
        pass

    def seen_message(self):
        pass

    def __str__(self) -> str:
        return f'{self.from_user} to {self.to_user} : {self.text}'


class NotificationModel(BaseModel, SoftDeleteModel):
    body = models.TextField()
    to_user = models.ForeignKey(User,
                                on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name, verbose_name_plural = _("Notification"), _("Notifications")
        db_table = 'Notification'

    def __str__(self) -> str:
        return f'{self.body} to user {self.to_user.username}'
    


