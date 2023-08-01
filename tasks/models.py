from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from accounts.models import User
# Create your models here.

class ListModel(models.Model):
    title = models.CharField(verbose_name=_("Title"),max_length=100,
                            help_text=_("Enter List title"))
    board = models.ForeignKey('Board', on_delete=models.CASCADE, related_name='lists')
    
    COLOR_CHOICES = [
        ('red',    'Red'),
        ('blue',   'Blue'),
        ('green',  'Green'),
        ('orange', 'Orange'),
        ('purple', 'Purple'),
        ('yellow', 'Yellow'),
    ]
    background_color = models.CharField(
        max_length=10,choices=COLOR_CHOICES, null=True, blank=True)
    
    class Meta:
        verbose_name, verbose_name_plural = _('List'), _('Lists')
        db_table = 'List'


class CardModel(BaseModel):
    title = models.CharField(verbose_name=_("Title"),max_length=150,
                             help_text=_("Enter Card title"))
    description = models.TextField(verbose_name=_("Description"),
                                   help_text=_("Enter card's description"),null=True,blank=True)
    
    start_date = models.DateTimeField(verbose_name=_("Start Time"),auto_now=True)
    due_date = models.DateTimeField(verbose_name=_("Due Time"),auto_now=True)
    reminder_time = models.DateTimeField(verbose_name=_("Reminder Time"),auto_now=True)
    has_reminder = models.BooleanField(default=False)
    
    list = models.ForeignKey(ListModel, on_delete=models.CASCADE, related_name='cards')
    
    STATUS_CHOICES = [
    ('todo', 'Todo'),
    ('doing','Doing'),
    ('done', 'Done'),
    ('suspended','Suspended'),
    ]
    status = models.CharField(
        max_length=20,choices=STATUS_CHOICES, default='todo')
    
    background_img = models.ImageField(upload_to='tasks', null=True, blank=True)
    
    class Meta:
        verbose_name, verbose_name_plural = _('Card'), _('Cards')
        db_table = 'Card'


class SubTaskModel(models.Model):
    title = models.CharField(verbose_name=_('Title'),
                             max_length=250,
                             help_text=_('Please enter your sub task title'))
    card = models.ForeignKey(CardModel, on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name=_('Status'),
                                 default=False,
                                 help_text=_('Sub Task status'))

    class Meta:
        verbose_name, verbose_name_plural = _('SubTask'), _('SubTasks')
        db_table = 'SubTask'


class CardCommentModel(models.Model):
    body = models.TextField(verbose_name=_('Body'),
                            help_text=_('comment on card'))
    card = models.ForeignKey(CardModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name, verbose_name_plural = _('Comment'), _('Comments')
        db_table = 'CardComment'


class LabelModel(models.Model):
    title = title = models.CharField(verbose_name=_("Title"),max_length=50,
                                     help_text=_("Enter Label title"))
    COLOR_CHOICES = [
        ('red',    'Red'),
        ('blue',   'Blue'),
        ('green',  'Green'),
        ('orange', 'Orange'),
        ('purple', 'Purple'),
        ('yellow', 'Yellow'),
    ]
    background_color = models.CharField(max_length=10,choices=COLOR_CHOICES,
                                         null=True, blank=True)
    card = models.ForeignKey(CardModel, on_delete=models.CASCADE, related_name='labels')
    
    class Meta:
        verbose_name, verbose_name_plural = _('Label'), _('Labels')
        db_table = 'Label'

class WorkSpaceModel(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_("Title"),max_length=100,
                             help_text=_("Enter WorkSpace title"))
    category = models.CharField(max_length=50,blank=True,null=True)
    background = models.ImageField(upload_to='tasks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    
class BoardModel(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    workspace = models.ForeignKey(WorkSpaceModel, on_delete=models.CASCADE,
                                  related_name='boards')
    title = models.CharField(verbose_name=_("Title"),max_length=100,
                             help_text=_("Enter Board title"))
    
    category = models.CharField(max_length=50,blank=True,null=True)
    VISIBILITY_CHOICES = [
        ('public',   'Public'),
        ('privet',   'Privet'),
        ('workspace','Workspace')
    ]
    visibility = models.CharField(max_length=20,choices=VISIBILITY_CHOICES,
                                  default='workspace')
    background = models.ImageField(upload_to='tasks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name, verbose_name_plural = _('Board'), _('Boards')
        db_table = 'Board'

    