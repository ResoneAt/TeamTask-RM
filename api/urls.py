from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import card, accounts
from rest_framework.schemas import get_schema_view

router = routers.SimpleRouter()
router.register(r'card', card.CardViewSet, basename='card')
router.register(r'mycard', card.MyCardViewSet, basename='mycardviewset')
router.register(r'subcard', card.SubCardViewSet)
router.register(r'list', card.ListViewSet)
router.register(r'label', card.LabelViewSet)


app_name = 'api'
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('signup/', accounts.SignUpAPIView.as_view(), name='signup'),
]

urlpatterns += router.urls
