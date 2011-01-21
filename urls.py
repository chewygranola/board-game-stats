from django.conf.urls.defaults import *

urlpatterns = patterns('boardgames.views',
    (r'^$', 'index'),
    (r'^game/(?P<game_type_string>\S+)/$', 'gametypeview'),
    (r'^(?P<view_string>\S+)/$', 'view_select'),
    (r'^(?P<game_id>\d+)/$', 'detail'),

)
