from django.contrib import admin
from .models import BotUsers

@admin.register(BotUsers)
class BotUsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name']

