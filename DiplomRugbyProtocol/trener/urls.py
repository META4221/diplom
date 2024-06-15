from django.urls import path
from . import views

app_name='trener'

urlpatterns=[
    path('Teams/', views.teams_view,name='teams'),
    path('TeamDetail/<int:id>/', views.player_list,name='players_list'),
    path('add/<int:pk>/',views.player_add,name='player_add'),
    path('addTeam/',views.add_team,name='team_add'),
    path('edit_player/<int:pk>/',views.edit_player,name='edit_player'),
    path('edit_team/<int:pk>/',views.edit_team,name='edit_team'),
    path('delete/<int:pk>/',views.delete_player,name='delete')
]