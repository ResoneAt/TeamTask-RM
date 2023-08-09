from django.urls import path
from . import views

app_name = 'tasks'
urlpatterns = [
    path('mycards/', views.ShowMyCards.as_view(), name='show_my_cards'),
    path('edit_card/<int:card_id>/', views.CardEditView.as_view(), name='edit_card'),
    path('workspace/create/',views.CreateWorkSpaceView.as_view(),name='create_workspace'),
    path('workspace/<int:workspace_id>/edit/',views.EditWorkSpaceView.as_view(),name='edit_workspace'),
    path('workspace/<int:workspace_id>/board/create/',views.CreateBoardView.as_view(),name='create_board'),
    path('workspace/<int:workspace_id>/',views.ShowWorkSpaceView.as_view(),name='show_workspace'),
]
