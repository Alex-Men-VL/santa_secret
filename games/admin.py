from django.contrib import admin

from .models import Profile, Game


class UserInline(admin.TabularInline):
    model = Profile


class GameAdmin(admin.ModelAdmin):
    inlines = [
        UserInline,
    ]


admin.site.register(Profile)
admin.site.register(Game, GameAdmin)
