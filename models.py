from django.db import models

# Create your models here.

class Player(models.Model):

	def __unicode__(self):
		return self.player_name
	
	player_name = models.CharField(max_length=100)

class Game_Type(models.Model):
	
	def __unicode__(self):
		return self.game_type_name
		
	def hyphenated(self):
		return self.game_type_name.replace(' ', '-').lower()
	
	game_type_name = models.CharField(max_length=100)

class Game(models.Model):

	def __unicode__(self):
		return str(self.play_date) + str(self.game_type)
	
	game_type = models.ForeignKey(Game_Type)
	play_date = models.DateField('date played')

class Game_Score(models.Model):
	game = models.ForeignKey(Game)
	player = models.ForeignKey(Player)
	score = models.PositiveIntegerField()
	place = models.PositiveIntegerField()
	
	def __unicode__(self):
		return str(self.player) + str(self.score)
	
