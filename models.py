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
		
	def get_baseline(rating_type):
		baseline_list = []
		
	
	def calculate_ratings(self,baseline_list = []):
		score_list = self.game_score_set.all()
		rating_list = [0] * len(score_list)
		
		if baseline_list == []:
			baseline_list = [0] * len(score_list)
		
		for index, game_score in enumerate(score_list[:len(score_list)-1]):
			print str(game_score.player) + " has defeatded:"
			for index2, opponent in enumerate(score_list[index+1:]):
				print str(opponent.player) + str(index2)
				opp_index = index2 + index + 1
				#if lower ranked
				ranking_difference = abs(baseline_list[index] - baseline_list[opp_index])
				if baseline_list[index] < baseline_list[opp_index]:
					#diff factor
					d_factor = (250.0 + ranking_difference)/(2*250)
					print d_factor
					opp_d_factor = -d_factor
					
					#rating score
					n_score = 100 - ((float(opponent.score)/game_score.score) * 100)
					print n_score
				else:
					d_factor = (250.0 - ranking_difference)/(2*250)
					print d_factor
					opp_d_factor = -d_factor
					
					#rating score
					n_score = abs(100 - ((float(opponent.score)/game_score.score) * 100))/3
					print n_score
					opp_n_score = abs(((float(opponent.score)/game_score.score) * 100) - 100)/3
					print opp_n_score
					rating_list[index] = rating_list[index] + (d_factor * n_score)
					rating_list[opp_index] = rating_list[opp_index] + (opp_d_factor * opp_n_score)
					print rating_list
			#loop through opponents
		rating_list = map(round, rating_list)
		print rating_list
		return rating_list
	
	game_type = models.ForeignKey(Game_Type)
	play_date = models.DateField('date played')

class Game_Score(models.Model):
	game = models.ForeignKey(Game)
	player = models.ForeignKey(Player)
	score = models.PositiveIntegerField()
	place = models.PositiveIntegerField()
	
	def __unicode__(self):
		return str(self.player) + str(self.score)
		
class Game_Rating(models.Model):
	game_score = models.ForeignKey(Game_Score)
	player = models.ForeignKey(Player)
	#for rating_type, 1 = year, 2 = month, 3 = week
	rating_type = models.CharField(max_length=5)
	rating = models.PositiveIntegerField()
	
