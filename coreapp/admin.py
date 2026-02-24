from django.contrib import admin
from .models import Tournament, TournamentJoin, MatchSchedule, TeamRegistration, TeamPlayer
from .models import ContactMessage


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('title', 'entry_fee', 'start_date')


@admin.register(TournamentJoin)
class TournamentJoinAdmin(admin.ModelAdmin):
    list_display = ('user', 'tournament', 'joined_at')


@admin.register(MatchSchedule)
class MatchScheduleAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'match_date', 'room_id')


class TeamPlayerInline(admin.TabularInline):
    model = TeamPlayer
    extra = 4


@admin.register(TeamRegistration)
class TeamRegistrationAdmin(admin.ModelAdmin):
    list_display = ('team_name',  'tournament', 'payment_status','approval_status')
    list_filter = ('payment_status','approval_status')  

@admin.register(TeamPlayer)
class TeamPlayerAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'team', 'in_game_name')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
   
