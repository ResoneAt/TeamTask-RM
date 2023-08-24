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
    path('board/', board.BoardView.as_view(), name='show_board')
]+router.urls
