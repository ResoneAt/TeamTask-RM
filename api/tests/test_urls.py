from django.test import TestCase
from django.urls import resolve, reverse
from api.views.card import MyCardsAPIView, CardAPIView, CardCreateAPIView, CardUpdateAPIView, \
                        CardDeleteAPIView
from api.views.membership import AddMemberToWorkspaceAPIView, UpdateMembershipFromWorkspaceAPIView, \
RemoveMemberFromWorkspaceAPIView, WorkspaceMembersListAPIView


class TestUrlsCards(TestCase):
    def test_MyCardsAPIView(self):
        url = reverse('api:my-cards-list', args=('1',))
        self.assertEqual(resolve(url).func.view_class, MyCardsAPIView)

    def test_CardAPIView(self):
        url = reverse('api:card-detail', args=('1',))
        self.assertEqual(resolve(url).func.view_class, CardAPIView)

    def test_CardCreateAPIView(self):
        url = reverse('api:create-card', args=('1',))
        self.assertEqual(resolve(url).func.view_class, CardCreateAPIView)

    def test_CardUpdateAPIView(self):
        url = reverse('api:update-card', args=('1',))
        self.assertEqual(resolve(url).func.view_class, CardUpdateAPIView)

    def test_CardDeleteAPIView(self):
        url = reverse('api:delete-card', args=('1',))
        self.assertEqual(resolve(url).func.view_class, CardDeleteAPIView)

class TestUrlsMembership(TestCase):
    def test_AddMemberToWorkspaceAPIView(self):
        url = reverse('api:add_member_to_workspace', args=('1', '1'))
        self.assertEqual(resolve(url).func.view_class, AddMemberToWorkspaceAPIView)

    def test_UpdateMembershipFromWorkspaceAPIView(self):
        url = reverse('api:update_membership_from_workspace', args=('1',))
        self.assertEqual(resolve(url).func.view_class, UpdateMembershipFromWorkspaceAPIView)

    def test_RemoveMemberFromWorkspaceAPIView(self):
        url = reverse('api:remove_member_from_workspace', args=('1',))
        self.assertEqual(resolve(url).func.view_class, RemoveMemberFromWorkspaceAPIView)

    def test_WorkspaceMembersListAPIView(self):
        url = reverse('api:workspace_members_list', args=('1',))
        self.assertEqual(resolve(url).func.view_class, WorkspaceMembersListAPIView)
