from django.contrib import admin
from .models import TelegramUser

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'phone_number')
    search_fields = ('user_id', 'first_name', 'phone_number')