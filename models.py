from django.db import models

# Create your models here.

class Player(models.Model):

	def __unicode__(self):
		return self.player_name
	
	def summate_rating(self,rating_type):
		n = 0
		for i in Game_Rating.objects.filter(rating_type=rating_type,player=Player.objects.get(player_name=self.player_name)).order_by('game_score__game__play_date'):
			n = n + i.rating
		return n
	
	player_name = models.CharField(max_length=100)

class Game_Type(models.Model):
	
	def __unicode__(self):
		return self.game_type_name
		
	def hyphenated(self):
		return self.game_type_name.replace(' ', '-').lower()
	
	def games_by_year(self,year):
		return Game.objects.filter(game_type=Game_Type.objects.get(game_type_name=self.game_type_name),play_date__year=year).order_by('play_date')
	
	def games_by_month(self,year_month):
		#format for year_month = YYYY.MM
		year = year_month.split('.')[0]
		month = year_month.split('.')[1]
		
	game_type_name = models.CharField(max_length=100)
	game_type_abbr = models.CharField(max_length=3)

class Game(models.Model):

	def __unicode__(self):
		return str(self.play_date) + str(self.game_type)
		
	def get_baseline(self, rating_type):
		baseline_list = []
		score_list = self.game_score_set.all()
		
		for game_score in score_list:
			#print [game_score.game.play_date, game_score.player.player_name, rating_type]
			try:
				baseline_list.append(Game_Rating.objects.filter(game_score__game__play_date__lte=game_score.game.play_date,game_score__player__player_name__exact=game_score.player.player_name,rating_type__exact=rating_type).order_by('-game_score__game__play_date')[0].rating)
			except:
				baseline_list.append(0)
		#print rating_type
		#print baseline_list
		return baseline_list
		
	def calculate_rating(self,baseline_list = []):
		score_list = self.game_score_set.all()
		rating_list = [0] * len(score_list)
		
		if baseline_list == []:
			baseline_list = [0] * len(score_list)
		
		for index, game_score in enumerate(score_list[:len(score_list)-1]):
			#print str(game_score.player) + " has defeatded:"
			for index2, opponent in enumerate(score_list[index+1:]):
				#print str(opponent.player) + str(index2)
				opp_index = index2 + index + 1
				#if lower ranked
				ranking_difference = abs(baseline_list[index] - baseline_list[opp_index])
				if baseline_list[index] < baseline_list[opp_index]:
					#diff factor
					d_factor = (250.0 + ranking_difference)/(2*250)
					#print d_factor
					opp_d_factor = -d_factor
					
				else:
					d_factor = (250.0 - ranking_difference)/(2*250)
					#print d_factor
					opp_d_factor = -d_factor
					
				#rating score
				n_score = abs(100 - ((float(opponent.score)/game_score.score) * 100))/3
				#print n_score
				opp_n_score = abs(((float(opponent.score)/game_score.score) * 100) - 100)/3
				#print opp_n_score
				rating_list[index] = rating_list[index] + (d_factor * n_score)
				rating_list[opp_index] = rating_list[opp_index] + (opp_d_factor * opp_n_score)
				#print rating_list
			#loop through opponents
		rating_list = map(round, rating_list)
		#print rating_list
		return rating_list
	
	def insert_rating(self, rating_type_string, baseline_list = []):
		n = self.calculate_rating(baseline_list)
		for index, score in enumerate(self.game_score_set.all()):
			s = Game_Rating(game_score=score,player=Player.objects.get(id=score.player.id), rating_type=rating_type_string, rating=n[index])
			s.save()
		#print n
	
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
	def __unicode__(self):
		return str(self.player) + '_' + str(self.rating_type) + '_' + str(self.rating)

	game_score = models.ForeignKey(Game_Score)
	player = models.ForeignKey(Player)
	#for rating_type, 1 = year, 2 = month, 3 = week
	rating_type = models.CharField(max_length=14)
	rating = models.FloatField()
	
