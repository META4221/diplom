from django.contrib import admin
from .models import Team, Player, PlayerDetails, Injuries

# Register your models here.
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display=['Name','TShirts','Pants','City','Trener']

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display=['FName','SName','LName', 'Team', 'Number', 'Capitan']

@admin.register(PlayerDetails)
class PlayerDetailsAdmin(admin.ModelAdmin):
    list_display=['playerId','change','attempts','realization','penalty','dropgols']

@admin.register(Injuries)
class InjuriesAdmin(admin.ModelAdmin):
    list_display=['PlayerID','Details']