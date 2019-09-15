from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from league_site.models import Team, Player, Weekend, Match
from django.views.generic import (View, TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from . import models
# from django.http import HttpResponse

# Create your views here.


class IndexView(TemplateView):
    template_name = 'home_page.html'

    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['injectme'] = 'BASIC INJECTION'
    #     return context


# def index(request):
#     return render(request,"home_page.html")

class MenTeamListView(ListView):
    context_object_name = 'teams'
    model = models.Team
    template_name = 'team_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['gender'] = "Men's"
        return context

    def get_queryset(self):
        queryset = Team.objects.all().filter(gender='M')
        return queryset

class WomenTeamListView(ListView):
    context_object_name = 'teams'
    model = models.Team
    template_name = 'team_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['gender'] = "Ladies'"
        return context

    def get_queryset(self):
        queryset = Team.objects.all().filter(gender='F')
        return queryset
    # school_list (this is what is returns)

class TeamDetailView(DetailView):
    context_object_name = 'team_detail'
    model = models.Team
    template_name = 'team_detail.html'

    def get_context_data(self, *args, **kwargs):
        team = self.get_object()
        context = super(TeamDetailView, self).get_context_data(*args, **kwargs)
        context['player_list'] =  Player.objects.filter(team = team)
        # context['player_list_2'] =  Player.objects.filter(team = self.name)[11:]
        return context

class PlayerDetailView(DetailView):
    context_object_name = 'player_detail'
    model = models.Player
    template_name = 'player_detail.html'

    # player_count = Team.objects.filter(player__team=pk).count()
    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['i'] =  1
    #     return context


class MenLogTableView(ListView):
    context_object_name = 'log_list'
    model = Team
    template_name = 'log.html'

    def get_queryset(self):
        # return Team.objects.filter(gender = 'M').order_by('-points','-goal_difference')
        return Team.objects.all().order_by('-points','-goal_difference')

class WomenLogTableView(ListView):
    context_object_name = 'log_list'
    model = Team
    template_name = 'log.html'

    def get_queryset(self):
        return Team.objects.filter(gender = 'F').order_by('-points')

class FantasyTableView(ListView):
    # context_object_name = 'fantasy_list'
    model = Player
    template_name = 'fantasy_log.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FantasyTableView, self).get_context_data(*args, **kwargs)
        context['fantasy_list_d'] =  Player.objects.filter(position = "Defender").order_by('-fantasy_points')[:10]
        context['fantasy_list_m'] =  Player.objects.filter(position = "Midfield").order_by('-fantasy_points')[:10]
        context['fantasy_list_f'] =  Player.objects.filter(position = "Forward").order_by('-fantasy_points')[:10]
        return context

    def get_queryset(self):
        return Player.objects.all().order_by('-fantasy_points')

class FantasyTeamView(ListView):
    model = Player
    template_name = 'fantasy_team.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FantasyTeamView, self).get_context_data(*args, **kwargs)
        context['fantasy_list_d'] =  Player.objects.filter(position = "Defender").order_by('-fantasy_points')[:4]
        context['fantasy_list_m'] =  Player.objects.filter(position = "Midfield").order_by('-fantasy_points')[:4]
        context['fantasy_list_f'] =  Player.objects.filter(position = "Forward").order_by('-fantasy_points')[:3]
        return context


class CreateTeamView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'team_detail.html'
    model = Team

class TeamUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    # form_class = PostForm ## Check what happens when you remove this.
    model = Team

# class PostDeleteView(LoginRequiredMixin,DeleteView):
#     model = Post
#     success_url = reverse_lazy('post_list')

class FixturesView(ListView):
    context_object_name = 'fixtures'
    model = Match
    template_name = 'fixtures.html'

    def get_queryset(self):
        return Match.objects.all().order_by('-date','time')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username') # getting the 'name' from the html file
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("SOMEONE TRIED TO LOGIN AND FAILED")
            print("Username: {} and password {}".format(username,password))
            return render(request,'login.html',{'error':"Incorrect email or password"})

    else:
        return render(request,'login.html',{'error':""})
