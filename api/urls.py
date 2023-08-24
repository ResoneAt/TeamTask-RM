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
app_name = 'api'

router = routers.SimpleRouter()
router.register(r'user', accounts.UserViewSet, basename='user')
router.register(r'notification', accounts.NotificationViewSet, basename='notification')
router.register(r'card', card.CardViewSet, basename='card')
router.register(r'mycard', card.MyCardViewSet, basename='mycardviewset')
router.register(r'subcard', card.SubCardViewSet)
router.register(r'list', card.ListViewSet)
router.register(r'label', card.LabelViewSet)

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('signup/', accounts.SignUpAPIView.as_view(), name='signup'),

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

]+router.urls
