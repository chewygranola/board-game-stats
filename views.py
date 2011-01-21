from boardgames.models import Player, Game_Type, Game, Game_Score
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render_to_response, get_object_or_404
# ...

def index(request):
    return render_to_response('boardgames/index.html')
    
def view_select(request, view_string):
	if view_string == 'game':
		game_type_list = Game_Type.objects.all().order_by('id')
		#output = ', '.join([str(g.game_type) for g in latest_game_list])
		#return HttpResponse(output)
		return render_to_response('boardgames/index.html', {'game_type_list': game_type_list})
	elif view_string == 'standings':
		return standingsview(request, 'home')

def standingsview(request, view_by):
	g = get_object_or_404(Game, pk=12)
	return render_to_response('boardgames/standings.html', {'game': g})	
    
def detail(request, game_id):
    g = get_object_or_404(Game, pk=game_id)
    return render_to_response('boardgames/detail.html', {'game': g})

def gametypeview(request, game_type_string):
	if game_type_string == 'all':
		game_type_list = Game.objects.all().order_by('-play_date')
	else:
		game_type_string = game_type_string.replace('-',' ')
		game_type_id = Game_Type.objects.get(game_type_name__iexact=game_type_string).id
		game_type_list = Game.objects.filter(game_type=game_type_id).order_by('-play_date')
    #output = ', '.join([str(g.game_type) for g in latest_game_list])
    #return HttpResponse(output)
	return render_to_response('boardgames/gametype.html', {'game_type_list': game_type_list})