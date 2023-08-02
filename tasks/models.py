from django.db import models
from core.models import BaseModel,SoftDeleteModel
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from django.urls import reverse
from django.utils import timezone
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
        
    def __str__(self) -> str:
        return f'{self.title}'
    
    def cards_count(self):
        return self.cards.count() 
    
    def get_ordered_cards(self):
        return self.cards.order_by('status', 'due_date')
    
    def get_completed_cards(self):
        return self.cards.filter(status='done')

    def get_incomplete_cards(self):
        return self.cards.exclude(status='done')

    def edit_list(self, title=None, background_color=None):
        try:
            if title is not None:
                self.title = title
            if background_color is not None:
                self.background_color = background_color
            self.save()
            return True
        except Exception as e:
            print(f"Error editing list: {e}")
            return False



class CardModel(BaseModel,SoftDeleteModel):
    title = models.CharField(verbose_name=_("Title"),max_length=150,
                             help_text=_("Enter Card title"))
    description = models.TextField(verbose_name=_("Description"),
                                   help_text=_("Enter card's description"),null=True,blank=True)
    
    start_date = models.DateTimeField(verbose_name=_("Start Time"),auto_now=True, null=True, blank=True)
    due_date = models.DateTimeField(verbose_name=_("Due Time"),auto_now=True, null=True, blank=True)
    reminder_time = models.DateTimeField(verbose_name=_("Reminder Time"),auto_now=True, null=True, blank=True)
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
        
    def __str__(self) -> str:
        return f'{self.title}'
    
    def get_absolut_url(self):
        return reverse('tasks:card_detail', args=(self.pk)) 
       
    def get_comments(self):
        return CardCommentModel.objects.filter(card=self)
    
    def move_card_to_new_list(self, new_list_id):
        try:
            new_list = ListModel.objects.get(id=new_list_id)
        except ListModel.DoesNotExist:
            raise ValueError('Invalid list ID')
        self.list.cards.remove(self)  # remove the card from the current list
        self.list = new_list  # set the new list for the card
        self.save() 

    def edit_card(self, title=None, description=None, status=None,
                  due_date=None, reminder_time=None, has_reminder=None):

        try:
            if title is not None:
                self.title = title
            if description is not None:
                self.description = description
            if status is not None:
                self.status = status
            if due_date is not None:
                self.due_date = due_date
            if has_reminder is not None:
                self.has_reminder = has_reminder
                if reminder_time is not None:
                    self.reminder_time = reminder_time
            self.save()
            return True
        except Exception as e:
            print(f"Error editing card: {e}")
            return False


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


class CardCommentModel(BaseModel):
    body = models.TextField(verbose_name=_('Body'),
                            help_text=_('comment on card'))
    card = models.ForeignKey(CardModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name, verbose_name_plural = _('Comment'), _('Comments')
        db_table = 'CardComment'
        
    def __str__(self) -> str:
        return f'Comment by {self.user} on {self.card.title}'
    
    def edit_comment(self, body):
        try:
            self.text = body
            self.save()
            return True
        except Exception as e:
            print(f"Error editing comment: {e}")
            return False


class LabelModel(models.Model):
    title = models.CharField(verbose_name=_("Title"),max_length=50,
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
    
    def get_absolute_url(self):
        return reverse('label_detail', args=[str(self.id)])
    
    def check_emergency(self):
        if self.card.due_date - timezone.now() < timezone.timedelta(hours=12):
            self.title = 'Emergency to do'
            self.background_color = 'red'
            self.save()

class WorkSpaceModel(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_("Title"),max_length=100,
                             help_text=_("Enter WorkSpace title"))
    category = models.CharField(max_length=50,blank=True,null=True)
    background = models.ImageField(upload_to='tasks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('workspace_detail', args=[str(self.id)])

    
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
    def get_absolute_url(self):
        return reverse('board_detail', args=[str(self.id)])
    
class CMembershipModel(BaseModel):
    user_parent = models.ForeignKey(User, on_delete=models.PROTECT)
    card_parent = models.ForeignKey(CardModel, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Membership in Card'
        verbose_name_plural = 'Card Memberships'
        db_table = 'card_membership'


class BMembershipModel(BaseModel):
    user_parent = models.ForeignKey(User, on_delete=models.PROTECT)
    board_parent = models.ForeignKey(BoardModel, on_delete=models.PROTECT)
    permission = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Membership in Board'
        verbose_name_plural = 'Board Memberships'
        db_table = 'board_membership'


class WSMembershipModel(BaseModel):
    user_parent = models.ForeignKey(User, on_delete=models.PROTECT)
    workspace_parent = models.ForeignKey(WorkSpaceModel, on_delete=models.PROTECT)
    permission = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Membership in Workspace'
        verbose_name_plural = 'Workspace Memberships'
        db_table = 'workspace_membership'
