from django.urls import path
from .views import telegram_auth, profile_view

urlpatterns = [
    path('api/auth/', telegram_auth, name='telegram-auth'),
    path('api/profile/', profile_view, name='profile'),
    # Boshqa URLlar...
]