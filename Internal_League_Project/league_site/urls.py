from django.urls import path, include
from league_site import views


app_name = 'league_site'

urlpatterns = [
    path('', views.IndexView.as_view(),name='home'),
    path('men_teams/',views.MenTeamListView.as_view(),name='men_team_list'),
    path('women_teams/',views.WomenTeamListView.as_view(),name='women_team_list'),
    path('team/<int:pk>/',views.TeamDetailView.as_view(), name='team_detail'),
    path('player/<int:pk>/',views.PlayerDetailView.as_view(), name='player_detail'),
    path('men_log/',views.MenLogTableView.as_view(),name='men_log'),
    path('women_log/',views.WomenLogTableView.as_view(),name='women_log'),
    path('fantasy/standings',views.FantasyTableView.as_view(),name='fantasy_log'),
    path('fantasy/team',views.FantasyTeamView.as_view(),name='fantasy_team'),
    path('team/new/',views.CreateTeamView.as_view(),name='team_new'),
    path('team/<int:pk>/edit/',views.TeamUpdateView.as_view(),name='team_edit'),
    path('fixtures/',views.FixturesView.as_view(),name='fixtures'),
]
