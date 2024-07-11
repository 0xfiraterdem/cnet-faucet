from django.urls import path
from .views import faucet

urlpatterns = [
    path('faucet/', faucet, name='faucet'),
]
