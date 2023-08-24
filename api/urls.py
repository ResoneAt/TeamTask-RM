from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

router = routers.SimpleRouter()
router.register(r'subcard', views.card.SubCardViewSet)
router.register(r'list', views.card.ListViewSet)
router.register(r'label', views.card.LabelViewSet)


app_name = 'api'
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #Card
    path('cards/<int:user_id>/my-cards/', views.MyCards.as_view(), name='my-cards-list'),
    path('boards/<int:board_id>/cards/', views.CardsView.as_view(), name='board-cards-list'),
    path('cards/<int:card_id>/', views.CardView.as_view(), name='card-detail'),
    path('cards/<int:list_id>/create-card/', views.CardCreate.as_view(), name='create-card'),
    path('cards/<int:card_id>/update/', views.CardUpdate.as_view(), name='update-card'),
    path('cards/<int:card_id>/delete/', views.CardDelete.as_view(), name='delete-card'),
]

urlpatterns += router.urls
