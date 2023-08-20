from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import CardModel, WorkSpaceModel, BoardModel, ListModel
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CardCreateEditForm, WorkSpaceForm, BoardForm, UsernameSearch
from accounts.models import User
from .models import RelationAddMemeber


class MyCardsView(LoginRequiredMixin, View):
    template_name = 'tasks/my_cards.html'
    
    def get(self, request):
        
        complete_cards = CardModel.get_completed_cards(request.user)
        incomplete_cards = CardModel.get_incomplete_cards(request.user)
        context = {
            'complete_cards': complete_cards,
            'incomplete_cards': incomplete_cards
        }
        return render(request, self.template_name, context)
   
    
class CardEditView(LoginRequiredMixin, View):
    card_instance: object
    template_name = 'tasks/card_edit.html'
    form_class = CardCreateEditForm

    def setup(self, request, *args, **kwargs):
        self.card_instance = get_object_or_404(CardModel, pk=kwargs['card_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        card = self.card_instance
        form = self.form_class(instance=card)
        return render(request, self.template_name, {'form': form, 'my_card': card})

    def post(self, request):
        card = self.card_instance
        form = self.form_class(request.POST, request.FILES, instance=card)

        if form.is_valid():
            form.save()
            messages.success(request, 'Edit card successfully', 'success')
            return redirect('show_my_cards')

        return render(request, self.template_name, {'form': form, 'card': card})


class WorkSpaceView(View):
    template_name = 'tasks/workspace.html'

    def get(self, request, workspace_id):
        workspace = get_object_or_404(WorkSpaceModel, pk=workspace_id)
        return render(request, self.template_name, {'workspace': workspace})


class WorkSpaceCreateView(LoginRequiredMixin, View):
    template_name = 'tasks/create_workspace.html'
    form_class = WorkSpaceForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            workspace = form.save(commit=False)
            workspace.owner = request.user
            workspace.save()
            messages.success(request, 'create workspace successfully', 'success')
            return redirect(workspace.get_absolute_url())
        return render(request, self.template_name, {'form': form})


class WorkSpaceEditView(LoginRequiredMixin, View):
    workspace_instance: object
    template_name = 'tasks/edit_workspace.html'
    form_class = WorkSpaceForm

    def setup(self, request, *args, **kwargs):
        self.workspace_instance = get_object_or_404(WorkSpaceModel,
                                                    pk=kwargs['workspace_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        workspace = self.workspace_instance
        form = self.form_class(instance=workspace)
        return render(request, self.template_name, {'form': form, 'workspace': workspace})

    def post(self, request):
        workspace = self.workspace_instance
        form = WorkSpaceForm(request.POST, request.FILES, instance=workspace)
        if form.is_valid():
            form.save()
            messages.success(request, 'edit workspace successfully', 'success')
            return redirect(workspace.get_absolute_url())
        return render(request, self.template_name, {'form': form, 'workspace': workspace})


class BoardView(LoginRequiredMixin, View):
    template_name = 'tasks/board.html'

    def get(self, request, board_id):
        board = get_object_or_404(BoardModel, pk=board_id)
        return render(request, self.template_name, {'board': board})


class BoardCreateView(LoginRequiredMixin, View):
    workspace_instance: object
    template_name = 'tasks/create_board.html'

    def setup(self, request, *args, **kwargs):
        self.workspace_instance = get_object_or_404(WorkSpaceModel,
                                                    pk=kwargs['workspace_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        form = BoardForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BoardForm(request.POST, request.FILES)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.workspace = self.workspace_instance
            board.save()
            messages.success(request, 'create Board successfully', 'success')
            return redirect(board.get_absolute_url())
        return render(request, self.template_name, {'form': form})


class WorkSpaceDeleteView(LoginRequiredMixin, View):
    template_name = 'tasks/delete_workspace.html'

    def setup( self, request, *args, **kwargs):
        self.workspace_instance = get_object_or_404(WorkSpaceModel,
                                                    pk=kwargs['workspace_id'])
        return super().setup(request, *args, **kwargs)

    def get(self,request):
        workspace = self.workspace_instance
        return render(request, self.template_name, {'workspace':workspace}) 

    def post(self, request):
        workspace = self.workspace_instance
        workspace.delete()
        messages.success(request, 'You delete workspace successfully', 'success')
        return redirect('home')


class WorkspaceMembersView(LoginRequiredMixin, View):
    template_name = 'tasks/workspace_members.html'


class BoardEditView(LoginRequiredMixin, View):
    template_name = 'tasks/board_edit.html'


class BoardDeleteView(LoginRequiredMixin, View):
    template_name = 'tasks/board_delete.html'


class BoardMembersView(LoginRequiredMixin, View):
    template_name = 'tasks/board_members.html'


class ListCreateView(LoginRequiredMixin, View):
    template_name = 'tasks/list_create.html'


class ListEditView(LoginRequiredMixin, View):
    template_name = 'tasks/list_create.html'


class ListDeleteView(LoginRequiredMixin, View):
    template_name = 'tasks/list_delete.html'


class CardCreateView(LoginRequiredMixin, View):
    list_instance : object
    template_name = 'tasks/card_create.html'
    form_class = CardCreateEditForm

    def setup(self, request, *args, **kwargs):
        self.list_instance = get_object_or_404(ListModel,
                                                pk=kwargs['list_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_card = form.save(commit=False)
            new_card.list = self.list_instance
            new_card.save()
            messages.success(request, 'you created a new card', 'success')
            return redirect(new_card.get_absolute_url())
        return render(request, self.template_name, {'form': form})


class CardDeleteView(LoginRequiredMixin, View):
    template_name = 'tasks/card_delete.html'


class LabelCreateView(LoginRequiredMixin, View):
    template_name = 'tasks/label_create.html'


class LabelEditView(LoginRequiredMixin, View):
    template_name = 'tasks/label_create.html'


class LabelDeleteView(LoginRequiredMixin, View):
    ...


class SubCardCreateView(LoginRequiredMixin, View):
    template_name = 'tasks/sub_card_create.html'


class SubCardEditView(LoginRequiredMixin, View):
    template_name = 'tasks/sub_card_create.html'


class SubCardDeleteView(LoginRequiredMixin, View):
    ...


# mohammad
class AddMemberToWorkspaceView(LoginRequiredMixin, View):
    template_name = 'tasks/add_member_workspace.html'

    def get(self, request):
        users = User.objects.all()
        if request.GET.get('search'):
            users = users.filter(username=request.GET['search'])

        user = User.objects.get(pk=user_id)
        add_memeber = RelationAddMemeber.objects.filter(from_user=request.user, to_add_user=user)
        if add_memeber.exists():
            messages.error(request, 'you already user in weorkspace', 'warning')
        else:
            RelationAddMemeber.objects.create(from_user=request.user, to_add_user=user)
            messages.success(request, 'you success add user in workspace', 'success')
        context = {
            'users': users
        }
        return self.render_to_response(context)
        

class RemoveMemberFromWorkspaceView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        add_memeber = RelationAddMemeber.objects.filter(from_user=request.user, to_add_user=user)
        if add_memeber.exists():
            add_memeber.delete()
            messages.success(request, 'you sucess remove member in workspace', 'success')
        else:
            return None
        


class ChangeWorkspaceMembershipPermissionView(LoginRequiredMixin, View):
    template_name = 'tasks/change_membership_permission.html'


class AddMemberToBoardView(LoginRequiredMixin, View):
    template_name = 'tasks/add_member.html'
	# template_name = 'tasks/add_member_workspace.html'
    def get(self, request):
	    user = User.object.all()
	    if request.GET.get('search'):
		    user = user.filter(username=request.GET['search'])
		    context = {
		        'user' : user
		        }
		    return render(request, self.template_name, context)

class RemoveMemberFromBoardView(LoginRequiredMixin, View):
    ...


class ChangeBoardMembershipPermissionView(LoginRequiredMixin, View):
    template_name = 'tasks/change_membership_permission.html'


class AddMemberToCardView(LoginRequiredMixin, View):
    template_name = 'tasks/add_member.html'
	# template_name = 'tasks/add_member_workspace.html'
    def get(self, request):
        user = User.object.all()
        if request.GET.get('search'):
            user = user.filter(username=request.GET['search'])
            context = {
                'user' : user
                }
            return render(request, self.template_name, context)

class RemoveMemberFromCardView(LoginRequiredMixin, View):
    ...

# end mohammad

