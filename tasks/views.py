from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import CardModel, WorkSpaceModel, BoardModel
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CardEditForm, WorkSpaceForm, BoardForm


class MyCardsView(LoginRequiredMixin, View):
    template_name = 'show_my_cards.html'
    
    def get(self, request):
        
        complete_cards = CardModel.get_completed_cards(request.user)
        incomplete_cards = CardModel.get_incomplete_cards(request.user)
        context = {
            'complete_cards': complete_cards,
            'incomplete_cards': incomplete_cards
        }
        return render(request, self.template_name, context)
   
    
class CardEditView(LoginRequiredMixin, View):
    template_name = 'card_edit.html'
    form_class = CardEditForm

    def setup(self, request, *args, **kwargs):
        self.card_instance = get_object_or_404(CardModel, pk=kwargs['card_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, **kwargs):
        card = self.card_instance
        form = self.form_class(instance=card)
        return render(request, self.template_name, {'form': form, 'my_card': card})

    def post(self, request, **kwargs):
        card = self.card_instance
        form = self.form_class(request.POST, request.FILES, instance=card)

        if form.is_valid():
            form.save()
            messages.success(request, 'Edit card successfully', 'success')
            return redirect('show_my_cards')

        return render(request, self.template_name, {'form': form, 'card': card})


class WorkSpaceCreateView(LoginRequiredMixin, View):
    template_name = 'create_workspace.html'
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
            return redirect(workspace.get_absolute_url())
        return render(request, self.template_name, {'form': form})


class WorkSpaceEditView(LoginRequiredMixin, View):
    template_name = 'edit_workspace'
    form_class = WorkSpaceForm

    def setup(self, request, *args, **kwargs):
        self.workspace_instance = get_object_or_404(WorkSpaceModel,
                                                    pk=kwargs['workspace_id'])

    def get(self, request, **kwargs):
        workspace = self.workspace_instance
        form = self.form_class(instance=workspace)
        return render(request, self.template_name, {'form': form, 'workspace': workspace})

    def post(self, request, **kwargs):
        workspace = self.workspace_instance
        form = WorkSpaceForm(request.POST, request.FILES, instance=workspace)
        if form.is_valid():
            form.save()
            messages.success(request, 'edit workspace successfully')
            return redirect(workspace.get_absolute_url())
        return render(request, self.template_name, {'form': form, 'workspace': workspace})


class CreateBoardView(LoginRequiredMixin, View):
    template_name = 'create_board.html'

    def get(self,request,workspace_id):
        workspace = WorkSpaceModel.objects.get(pk=workspace_id,owner=request.user)
        form = BoardForm()
        return render(request,self.template_name,{'form':form,'workspace':workspace})

    def post(self,request,workspace_id):
        workspace = WorkSpaceModel.objects.get(pk=workspace_id, owner=request.user)
        form = BoardForm(request.POST,request.FILES)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.workspace = workspace
            board.save()
            return redirect(board.get_absolute_url())
        return render(request,self.template_name,{'form':form,'workspace':workspace})

class ShowWorkSpaceView(View):
    template_name = 'show_workspace.html'

    def get(self,request,workspace_id):
        workspace = get_object_or_404(WorkSpaceModel,pk=workspace_id)
        return render(request,self.template_name,{'workspace':workspace})

class ShowBoardView(LoginRequiredMixin,View):
    template_name = 'show_board.html'

    def get(self,request,board_id):
        board = BoardModel.objects.get(pk=board_id,owner=request.user)
        return render(request,self.template_name,{'board':board})
