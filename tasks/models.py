from django.db import models
from core.models import BaseModel,SoftDeleteModel
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q


class ListModel(BaseModel, SoftDeleteModel):
    title = models.CharField(verbose_name=_("Title"),
                             max_length=100,
                             help_text=_("Enter List title"),
                             db_index=True)
    board = models.ForeignKey('BoardModel', on_delete=models.DO_NOTHING,
                              related_name='lists',
                              db_index=True)

    # we can write  instead'red' into '1' and max_lenght=1
    COLOR_CHOICES = [
        ('red',    'Red'),
        ('blue',   'Blue'),
        ('green',  'Green'),
        ('orange', 'Orange'),
        ('purple', 'Purple'),
        ('yellow', 'Yellow'),
    ]
    background_color = models.CharField(max_length=10,
                                        choices=COLOR_CHOICES,
                                        null=True, blank=True)
    
    class Meta:
        verbose_name, verbose_name_plural = _('List'), _('Lists')
        db_table = 'List'
        
    def __str__(self) -> str:
        return f'{self.title}'
    
    def cards_count(self):
        return self.cards.count() 
    
    def get_ordered_cards(self):
        return self.cards.order_by('status', 'due_date')


class CardModel(BaseModel, SoftDeleteModel):
    title = models.CharField(verbose_name=_("Title"),
                             max_length=150,
                             help_text=_("Enter Card title"),
                             db_index=True)
    description = models.TextField(verbose_name=_("Description"),
                                   help_text=_("Enter card's description"),
                                   null=True, blank=True)
    
    start_date = models.DateTimeField(verbose_name=_("Start Time"),
                                      auto_now=True,
                                      null=True, blank=True)
    due_date = models.DateTimeField(verbose_name=_("Due Time"),
                                    auto_now=True,
                                    null=True, blank=True)
    reminder_time = models.DateTimeField(verbose_name=_("Reminder Time"),
                                         auto_now=True,
                                         null=True, blank=True)
    has_reminder = models.BooleanField(default=False)
    
    list = models.ForeignKey(ListModel,
                             on_delete=models.DO_NOTHING,
                             related_name='cards',
                             db_index=True)

    STATUS_CHOICES = [
     ('todo', 'Todo'),
     ('doing', 'Doing'),
     ('done', 'Done'),
     ('suspended', 'Suspended'),
    ]
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='todo',
                              db_index=True)
    
    background_img = models.ImageField(upload_to='tasks',
                                       null=True, blank=True)

    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependent_cards')
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='prerequisite_cards')
    is_independent = models.BooleanField(default=True)

    class Meta:
        verbose_name, verbose_name_plural = _('Card'), _('Cards')
        db_table = 'Card'

    def __str__(self) -> str:
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('tasks:card_detail', args=[self.pk])

    def get_comments(self):
        return CardCommentModel.objects.filter(card=self)

    @staticmethod
    def get_completed_cards(user):
        return CardModel.objects.filter(status='done',
                                        user=user)

    @staticmethod
    def get_incomplete_cards(user):
        return CardModel.objects.filter(Q(status='doing', user=user) |
                                        Q(status='todo', user=user))

    def move_card_to_new_list(self, new_list_id):
        try:
            new_list = ListModel.objects.get(id=new_list_id)
        except ListModel.DoesNotExist:
            raise ValueError('Invalid list ID')
        self.list.cards.remove(self) 
        self.list = new_list  
        self.save() 

    def completion_percentage(self):
        total_cards = self.list.cards.count()
        completed_cards = self.list.cards.filter(status='done').count()
        if total_cards > 0:
            return (completed_cards / total_cards) * 100
        else:
            return 0

    def all_cards_completion_percentage():
        total_cards = CardModel.objects.all()
        completed_cards = CardModel.objects.filter(status='done').count()
        if total_cards > 0:
            return (completed_cards / total_cards) * 100
        else:
            return 0

    def add_prerequisite(self, prerequisite_card):
        self.prerequisites.add(prerequisite_card)

    def add_dependency(self, dependent_card):
        self.dependencies.add(dependent_card)

    def mark_as_independent(self):
        self.is_independent = True
        self.save()

    def mark_as_not_independent(self):
        self.is_independent = False
        self.save()

    def count_dependent_cards(self):
        return self.dependencies.count()


class SubTaskModel(models.Model):
    title = models.CharField(verbose_name=_('Title'),
                             max_length=250,
                             help_text=_('Please enter your sub task title'),
                             db_index=True)
    card = models.ForeignKey(CardModel,
                             on_delete=models.DO_NOTHING,
                             db_index=True)
    status = models.BooleanField(verbose_name=_('Status'),
                                 default=False,
                                 help_text=_('Sub Task status'))

    class Meta:
        verbose_name, verbose_name_plural = _('SubTask'), _('SubTasks')
        db_table = 'SubTask'


class CardCommentModel(BaseModel):
    body = models.TextField(verbose_name=_('Body'),
                            help_text=_('comment on card'))
    card = models.ForeignKey(CardModel, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                             db_index=True)
    
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
    title = models.CharField(verbose_name=_("Title"),
                             max_length=50,
                             help_text=_("Enter Label title"),
                             db_index=True)
    COLOR_CHOICES = [
        ('red',    'Red'),
        ('blue',   'Blue'),
        ('green',  'Green'),
        ('orange', 'Orange'),
        ('purple', 'Purple'),
        ('yellow', 'Yellow'),
    ]
    background_color = models.CharField(max_length=10,
                                        choices=COLOR_CHOICES,
                                        null=True, blank=True)
    card = models.ForeignKey(CardModel,
                             on_delete=models.DO_NOTHING,
                             related_name='labels',
                             db_index=True)
    
    class Meta:
        verbose_name, verbose_name_plural = _('Label'), _('Labels')
        db_table = 'Label'
    
    def get_absolute_url(self):
        return reverse('label_detail', args=[str(self.pk)])
    
    def check_emergency(self):
        if self.card.due_date - timezone.now() < timezone.timedelta(hours=12):
            self.title = 'Emergency to do'
            self.background_color = 'red'
            self.save()
    
    def edit_label(self, title=None, background_color=None):
        if title is not None:
            self.title = title
        if background_color is not None:
            self.background_color = background_color
        self.save()
    
    def __str__(self):
        return self.title


class WorkSpaceModel(BaseModel, SoftDeleteModel):
    owner = models.ForeignKey(User,
                              on_delete=models.DO_NOTHING,
                              db_index=True)
    title = models.CharField(verbose_name=_("Title"),
                             max_length=100,
                             help_text=_("Enter WorkSpace title"))
    category = models.CharField(max_length=50,
                                blank=True, null=True)
    background = models.ImageField(upload_to='tasks',
                                   blank=True, null=True)

    class Meta:
        verbose_name, verbose_name_plural = _('WorkSpace'), _('WorkSpaces')
        db_table = 'WorkSpace'

    def get_absolute_url(self):
        return reverse('workspace_detail', args=[str(self.id)])

    def edit_workspace(self,
                       title=None,
                       category=None,
                       background=None):

        if title is not None:
            self.title = title
        if category is not None:
            self.category = category
        if background is not None:
            self.background = background
        self.save()

    def __str__(self):
        return self.title


class BoardModel(BaseModel, SoftDeleteModel):
    owner = models.ForeignKey(User,
                              on_delete=models.DO_NOTHING,
                              db_index=True)
    workspace = models.ForeignKey(WorkSpaceModel,
                                  on_delete=models.DO_NOTHING,
                                  related_name='boards')
    title = models.CharField(verbose_name=_("Title"),
                             max_length=100,
                             help_text=_("Enter Board title"),
                             db_index=True)
    
    category = models.CharField(max_length=50,
                                blank=True, null=True)
    VISIBILITY_CHOICES = [
        ('public',    'Public'),
        ('privet',    'Privet'),
        ('workspace', 'Workspace')
    ]
    visibility = models.CharField(max_length=20,
                                  choices=VISIBILITY_CHOICES,
                                  default='workspace')
    background = models.ImageField(upload_to='tasks',
                                   blank=True, null=True)

    class Meta:
        verbose_name, verbose_name_plural = _('Board'), _('Boards')
        db_table = 'Board'

    def get_absolute_url(self):
        return reverse('board_detail', args=[str(self.id)])
    
    def edit_board(self, title=None,
                   category=None,
                   visibility=None,
                   background=None):

        if title is not None:
            self.title = title
        if category is not None:
            self.category = category
        if visibility is not None:
            self.visibility = visibility
        if background is not None:
            self.background = background
        self.save()
    
    def __str__(self):
        return self.title

    def count_board_cards(self):
        return self.cards.count()


class GMessageModel(BaseModel, SoftDeleteModel):
    from_user = models.ForeignKey(User,
                                  on_delete=models.DO_NOTHING,
                                  related_name='g_sender')
    text = models.TextField(help_text='Please Write Your Message')
    board = models.ForeignKey(BoardModel,
                              on_delete=models.DO_NOTHING,
                              db_index=True)

    class Meta:
        verbose_name, verbose_name_plural = _("GMessage"), _("GMessages")
        db_table = 'GroupMessage'

    def send_message(self):
        pass

    def seen_message(self):
        pass

    def __str__(self) -> str:
        return f'{self.from_user} : {self.text}'


class CMembershipModel(BaseModel):
    from_user = models.ForeignKey(User,
                                  on_delete=models.DO_NOTHING,
                                  related_name='card_admin',
                                  db_index=True)
    to_user = models.ForeignKey(User,
                                on_delete=models.DO_NOTHING,
                                related_name='card_user',
                                db_index=True)
    card = models.ForeignKey(CardModel,
                             on_delete=models.DO_NOTHING,
                             db_index=True)

    class Meta:
        verbose_name = 'Membership in Card'
        verbose_name_plural = 'Card Memberships'
        db_table = 'CardMembership'

    def __str__(self):
        return f'{self.to_user} - {self.card}'
    

class BMembershipModel(BaseModel):
    from_user = models.ForeignKey(User,
                                  on_delete=models.DO_NOTHING,
                                  related_name='board_admin',
                                  db_index=True)
    to_user = models.ForeignKey(User,
                                on_delete=models.DO_NOTHING,
                                related_name='board_user',
                                db_index=True)
    board = models.ForeignKey(BoardModel,
                              on_delete=models.DO_NOTHING,
                              db_index=True)
    permission = models.CharField(max_length=255, default='public')

    class Meta:
        verbose_name = 'Membership in Board'
        verbose_name_plural = 'Board Memberships'
        db_table = 'BoardMembership'

    def __str__(self):
        return f'{self.to_user} - {self.board}'
    

class WSMembershipModel(BaseModel):
    from_user = models.ForeignKey(User,
                                  on_delete=models.DO_NOTHING,
                                  related_name='workspace_admin',
                                  db_index=True)
    to_user = models.ForeignKey(User,
                                on_delete=models.DO_NOTHING,
                                related_name='workspace_user',
                                db_index=True)
    workspace = models.ForeignKey(WorkSpaceModel,
                                  on_delete=models.DO_NOTHING,
                                  db_index=True)
    permission = models.CharField(max_length=255, default='public')

    class Meta:
        verbose_name = 'Membership in Workspace'
        verbose_name_plural = 'Workspace Memberships'
        db_table = 'WorkspaceMembership'

    def __str__(self):
        return f'{self.to_user} - {self.workspace}'

    def count_workspace_members(self):
        return WSMembershipModel.objects.filter(workspace=self).count()


class RelationAddMemeber(BaseModel):
    from_user = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='admin',
                                  db_index=True)
    to_add_user = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    related_name='add',
                                    db_index=True)

    def __str__(self):
        return f'{self.from_user} - {self.to_add_user}'

    class Meta:
        verbose_name = 'relation-add-member'
        verbose_name_plural = 'relation-add-members'
        db_table = 'relation-add-member-model'