from django.urls import path
from . import views

app_name='referee'

urlpatterns=[
    path('addChange/<int:id>/', views.add_change,name='add_change_player'),
    path('addDelete/<int:id>/',views.add_delete,name='add_delete_player'),
    path('addAlert/<int:id>/',views.add_alert,name='add_alert_player'),
    path('addMatch/',views.add_match,name='add_match'),
    path('addGol/<int:id>/',views.add_gol,name='add_gol'),
    path('save/<int:id>/',views.save,name='save'),
    path('matchDetail/<int:id>/',views.matchDetail,name='teamA_alerts'),
    path('match/',views.match_list, name='match')
    # path('addMatch/')
]