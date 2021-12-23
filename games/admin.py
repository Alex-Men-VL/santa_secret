from django.contrib import admin

from .models import Profile, Game


class UserInline(admin.TabularInline):
    model = Profile


class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    inlines = [
        UserInline,
    ]


admin.site.register(Game, GameAdmin)
