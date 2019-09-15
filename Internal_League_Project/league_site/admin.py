from django.contrib import admin

from league_site.models import Team, Player, Weekend, Match

# Register your models here.
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Weekend)
admin.site.register(Match)
