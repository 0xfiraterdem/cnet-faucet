from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cnet_faucet.urls')),
]

handler404 = 'cnet_faucet.views.custom_404'
