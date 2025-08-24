from django.contrib import admin
from .models import User

# DE: Benutzer im Admin registrieren (mit eigener Admin-Klasse)
# RU: Регистрация пользователя в админке (с кастомным админ-классом)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "username", "is_active", "is_staff", "date_joined")
    list_filter = ("is_active", "is_staff", "date_joined")
    search_fields = ("email", "username")
    ordering = ("-date_joined",)