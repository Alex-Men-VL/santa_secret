from django.contrib import admin, messages


from .models import Profile, Game
from .email_utils import send_email_to_players


class UserInline(admin.TabularInline):
    model = Profile.games.through


class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_filter = ['draw_done']
    readonly_fields = ['slug']
    inlines = [
        UserInline,
    ]
    actions = ['draw_lots_by_admin']

    @admin.action(description='Провести жеребьевку')
    def draw_lots_by_admin(self, request, queryset):
        one_was_held = False
        for game in queryset:
            if game.draw_done:
                self.message_user(
                    request,
                    f'Жеребьевка игры (slug={game.slug}) уже была проведена.',
                    messages.ERROR
                )
                continue
            players = game.players.all()
            game.players_count = players.count()
            if game.players_count < 3:
                self.message_user(
                    request,
                    f'Для жеребьевки игры (slug={game.slug}) '
                    'недостаточно игроков.',
                    messages.ERROR
                )
                continue
            send_email_to_players(players, game)
            game.draw_done = True
            game.save()
            one_was_held = True

        if one_was_held:
            self.message_user(
                request,
                'Жеребьевка проведена',
                messages.SUCCESS
            )

    def save_model(self, request, obj, form, change):
        if obj.owner == request.user:
            if obj.owner in [user.user for user in obj.players.all()]:
                obj.owner_joined = True
            else:
                obj.owner_joined = False
        obj.save()
        super().save_model(request, obj, form, change)


class ProfileAdmin(admin.ModelAdmin):
    actions = ['add_permission']

    @admin.action(description='Сделать ассистентом')
    def add_permission(self, request, queryset):
        for person in queryset:
            user = person.user
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.message_user(
                request,
                f'Пользователь {user.username} получил права ассистента',
                messages.SUCCESS
            )


admin.site.register(Game, GameAdmin)
admin.site.register(Profile, ProfileAdmin)
