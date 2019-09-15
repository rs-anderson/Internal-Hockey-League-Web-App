from django.db import models
from django.db.models import Count
from datetime import date


# Create your models here.

from django.urls import reverse

# Create your models here.
class Team(models.Model):
    # played = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    goals_for = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField("Points (automatically calculated)",default=0)
    goal_difference = models.IntegerField("Goal Difference (automatically calculated)",default=0)


    A = 'A'
    B = 'B'
    POOL_CHOICES = (
            (A,'A'),
            (B,'B'),
    )
    pool = models.CharField(
            max_length=1,
            choices=POOL_CHOICES,
            default=A,
        )

    name = models.CharField(max_length=256)
    team_pic = models.ImageField(upload_to='team_pics',blank=True)
    jersey = models.ImageField(upload_to="jerseys",blank=True)
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=FEMALE,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('team_detail',kwargs={'pk':self.pk})

    def ranking(self):
        aggregate = Team.objects.filter(points__gt=self.points, gender=self.gender, pool=self.pool).aggregate(ranking=Count('points'))
        return aggregate['ranking'] + 1

    def played(self):
        return self.wins + self.draws + self.losses

    def save(self, *args, **kwargs):
        self.points = self.wins*3 + self.draws
        self.goal_difference = self.goals_for - self.goals_against
        super(Team, self).save(*args, **kwargs)



class Player(models.Model):
    name = models.CharField(max_length=256)
    team = models.ForeignKey(Team,related_name='players',on_delete=models.CASCADE)
    player_pic = models.ImageField(upload_to='player_pics',blank=True)

    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    clean_sheets = models.PositiveIntegerField(default=0)
    appearances = models.PositiveIntegerField(default=0)

    DEFENDER = 'Defender'
    MIDFIELD = 'Midfield'
    FORWARD = 'Forward'
    POSITION_CHOICES = (
        (DEFENDER, 'Defender'),
        (MIDFIELD, 'Midfield'),
        (FORWARD, 'Forward'),
    )
    position = models.CharField(
        max_length=8,
        choices=POSITION_CHOICES,
        default=DEFENDER,
    )

    fantasy_points = models.PositiveIntegerField("Fantasy Points (automatically calculated)",default=0)

    def __str__(self):
        return self.name

    def ranking(self):
        aggregate = Player.objects.filter(fantasy_points__gt=self.fantasy_points, position = self.position).aggregate(ranking=Count('fantasy_points'))
        return aggregate['ranking'] + 1

    def save(self, *args, **kwargs):
        if self.position == 'Defender':  ## Def: goals*6 assists*3 cleanSheets*5 ## Mid: goals*
            self.fantasy_points = self.goals*6 + self.assists*3 + self.clean_sheets*5 + self.appearances*2
        elif self.position == 'Midfield':
            self.fantasy_points = self.goals*5 + self.assists*3 + self.appearances*2
        else:
            self.fantasy_points = self.goals*4 + self.assists*3 + self.appearances*2
        super(Player, self).save(*args, **kwargs)

class Weekend(models.Model):
    date = models.DateField(default=date.today)

    def __str__(self):
        return str(self.date)

class Match(models.Model):
    team1 = models.ForeignKey(Team,related_name='match_team1',on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team,related_name='match_team2',on_delete=models.CASCADE)
    date = models.ForeignKey(Weekend,related_name='match_date',on_delete=models.CASCADE)
    time = models.TimeField(blank=True)
    team1_goals = models.IntegerField(default=-1)
    team2_goals = models.IntegerField(default=-1)
    score_recorded = models.BooleanField("score recorded - DO NOT TOUCH",default=False)

    class Meta:
        verbose_name_plural = "Matches"


    def __str__(self):
        return self.team1.name + " vs " + self.team2.name + " | " + str(self.time) + " (" + str(self.date) + ")"

    def updateStats(self):
        print("trigerred")

        self.team1.goals_for += self.team1_goals
        self.team2.goals_for += self.team2_goals
        self.team1.goals_against += self.team2_goals
        self.team2.goals_against += self.team1_goals

        if self.team1_goals > self.team2_goals:
            print(self.team1.wins)
            self.team1.wins = self.team1.wins + 1
            print(self.team1.wins)
            self.team2.losses += 1
            print("recorded1")
            self.team1.save()
            self.team2.save()
        elif self.team1_goals < self.team2_goals:
            self.team2.wins += 1
            self.team1.losses += 1
            print("recorded2")
            self.team1.save()
            self.team2.save()
        else:
            self.team1.draws += 1
            self.team2.draws += 1
            print("recorded3")
            self.team1.save()
            self.team2.save()


    def save(self, *args, **kwargs):
        if self.score_recorded==False and self.team1_goals!=-1:
            self.updateStats()
            self.score_recorded=True
        super(Match, self).save(*args, **kwargs)
