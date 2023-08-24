from django.urls import path
from rest_framework import routers
from .views import card, accounts
from .views import board
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
app_name = 'api'
router = routers.SimpleRouter()

router.register(r'user', accounts.UserViewSet, basename='user')
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
    path('board/', board.BoardListView.as_view(), name='all_board_workspace'),
    path('board/create/<int:pk>/', board.BoardCreateView.as_view(), name='create_board'),
    path('board/update/<int:pk>/', board.BoardUpdateView.as_view(), name='update_board'),
    path('board/delete/<int:pk>/', board.BoardDeleteView.as_view(), name='delete_board'),
]+router.urls
