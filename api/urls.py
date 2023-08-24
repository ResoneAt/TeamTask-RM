from django.urls import path
from rest_framework import routers
from .views import(
    card,
    accounts,
    membership
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'user', accounts.UserViewSet, basename='user')
router.register(r'notification', accounts.NotificationViewSet, basename='notification')
router.register(r'subcard', views.card.SubCardViewSet)
router.register(r'list', views.card.ListViewSet)
router.register(r'label', views.card.LabelViewSet)
router.register(r'subcard', card.SubCardViewSet)
router.register(r'list', card.ListViewSet)
router.register(r'label', card.LabelViewSet)

urlpatterns = [

    # accounts
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('signup/', accounts.SignUpAPIView.as_view(), name='signup'),

    # Card
    path('cards/<int:user_id>/my-cards/', views.MyCards.as_view(), name='my-cards-list'),
    path('boards/<int:board_id>/cards/', views.CardsView.as_view(), name='board-cards-list'),
    path('cards/<int:card_id>/', views.CardView.as_view(), name='card-detail'),
    path('cards/<int:list_id>/create-card/', views.CardCreate.as_view(), name='create-card'),
    path('cards/<int:card_id>/update/', views.CardUpdate.as_view(), name='update-card'),
    path('cards/<int:card_id>/delete/', views.CardDelete.as_view(), name='delete-card'),

    # membership
    path('add-member-to-workspace/<int:workspace_id>/<int:user_id>/',
         membership.AddMemberToWorkspaceAPIView.as_view(),
         name='add_member_to_workspace'),
    path('update-membership-from-workspace/<int:membership_id>/',
         membership.UpdateMembershipFromWorkspaceAPIView.as_view(),
         name='update_membership_from_workspace'),
    path('remove-member-from-workspace/<int:membership_id>/',
         membership.RemoveMemberFromWorkspaceAPIView.as_view(),
         name='remove_member_from_workspace'),
    path('workspace-members-list/<int:workspace_id>/',
         membership.WorkspaceMembersListAPIView.as_view(),
         name='workspace_members_list'),

    path('add-member-to-board/<int:board_id>/<int:user_id>/',
         membership.AddMemberToBoardAPIView.as_view(),
         name='add_member_to_board'),
    path('update-membership-from-board/<int:membership_id>/',
         membership.UpdateMembershipFromBoardAPIView.as_view(),
         name='update_membership_from_board'),
    path('remove-member-from-board/<int:membership_id>/',
         membership.RemoveMemberFromBoardAPIView.as_view(),
         name='remove_member_from_board'),
    path('board-members-list/<int:board_id>/',
         membership.BoardMembersListAPIView.as_view(),
         name='board_members_list'),

    path('add-member-to-card/<int:card_id>/<int:user_id>/',
         membership.AddMemberToCardAPIView.as_view(),
         name='add_member_to_card'),
    path('remove-member-from-card/<int:membership_id>/',
         membership.RemoveMemberFromCardAPIView.as_view(),
         name='remove_member_from_card'),
    path('card-members-list/<int:card_id>/',
         membership.CardMembersListAPIView.as_view(),
         name='card_members_list'),

              ]+router.urls
