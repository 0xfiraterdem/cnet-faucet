from django.contrib import admin
from .models import FaucetRequest


class FaucetRequestAdmin(admin.ModelAdmin):
    list_display = ('id','wallet_address','request_time')

admin.site.register(FaucetRequest, FaucetRequestAdmin)
