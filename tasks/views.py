from django.shortcuts import render,get_object_or_404, redirect
from django.views import View
from .models import CardModel, ListModel,WorkSpaceModel,BoardModel
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CardEditForm ,WorkSpaceForm ,BoardForm

# Create your views here.
class ShowMyCards(LoginRequiredMixin,View):
    template_name = 'show_my_cards.html'
    
    def get(self, request, *args, **kwargs):
        # cards = CardModel.objects.filter(user=request.user) 
        # return render(request, self.template_name, context={'cards': cards})
        lists = ListModel.objects.filter(user=request.user).prefetch_related('cards')
        return render(request, self.template_name, {'lists': lists})
        


class CardEditView(LoginRequiredMixin,View):
    template_name = 'card_edit.html'  
    form_class = CardEditForm

    def get(self, request, card_id):
        mycard = get_object_or_404(CardModel, id=card_id, user=request.user)
        form = self.form_class(instance=mycard)

        return render(request, self.template_name, {'form':form, 'mycard':mycard})

    def post(self, request, card_id):
        mycard = get_object_or_404(CardModel, id=card_id, user=request.user)

        form = self.form_class(request.POST, instance=mycard)

        if form.is_valid():
            form.save()
            return redirect('show_my_cards')   

        return render(request, self.template_name, {'form':form, 'mycard':mycard})

    
class CreateWorkSpaceView(LoginRequiredMixin,View):
    template_name = 'create_workspace.html'

    def get(self,request):
        form = WorkSpaceForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form = WorkSpaceForm(request.POST,request.FILES)
        if form.is_valid():
            workspace = form.save(commit=False)
            workspace.owner = request.user
            workspace.save()
            return redirect(workspace.get_absolute_url())
        return render(request,self.template_name,{'form':form})

class EditWorkSpaceView(LoginRequiredMixin,View):
    template_name = 'edit_workspace'

    def get(self,request,workspace_id):
        workspace = WorkSpaceModel.objects.get(pk=workspace_id,owner=request.user)
        form = WorkSpaceForm(isinstance=workspace)
        return render(request,self.template_name,{'form':form,'workspace':workspace})

    def post(self,request,workspace_id):
        workspace = WorkSpaceModel.objects.get(pk=workspace_id, owner=request.user)
        form = WorkSpaceForm(request.POST,request.FILES,isinstance=workspace)
        if form.is_valid():
            form.save()
            return redirect(workspace.get_absolute_url())
        return render(request,self.template_name,{'form':form,'workspace':workspace})

class CreateBoardView(LoginRequiredMixin,View):
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