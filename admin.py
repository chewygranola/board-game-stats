from boardgames.models import Player, Game_Type, Game, Game_Score
from django.contrib import admin

#admin.site.register(Player, Game_Type, Game, Game_Score)

class Game_ScoreInline(admin.TabularInline):
	fields = ['place','player','score']
	model = Game_Score
	max_num = 6

class GameAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['game_type','play_date']}),
	]
	
	inlines = [Game_ScoreInline]
	
admin.site.register(Game, GameAdmin)