from django.contrib import admin

from .models import BotUser


class BotUserAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'telegramId', 'telegramContact', 'selectedLevel', 'confirmedLevel', 'registeredAt']
    list_filter = ['selectedLevel', 'confirmedLevel', 'recommendedLevel']
    search_fields = ['telegramId', 'fullname', 'telegramContact', 'phoneNumber']


admin.site.register(BotUser, BotUserAdmin)
