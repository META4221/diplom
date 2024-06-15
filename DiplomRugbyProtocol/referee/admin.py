from django.contrib import admin
from .models import Match,MatchType,Aletrs,Deletes,Changes,Gols,GolsTypes

# Register your models here.
admin.site.register(Match)
admin.site.register(MatchType)
admin.site.register(Aletrs)
admin.site.register(Deletes)
admin.site.register(Changes)
admin.site.register(Gols)
admin.site.register(GolsTypes)