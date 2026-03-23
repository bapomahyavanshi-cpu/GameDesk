from django.db import models
from django.contrib.auth.models import User


class Tournament(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='tournaments/')
    entry_fee = models.IntegerField()
    prize_pool = models.CharField(max_length=100)
    start_date = models.DateField()

    def str(self):
        return self.title


class TournamentJoin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user.username} - {self.tournament.title}"


class MatchSchedule(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    match_date = models.DateTimeField()
    room_id = models.CharField(max_length=50, blank=True, null=True)
    room_password = models.CharField(max_length=50, blank=True, null=True)

    def str(self):
        return f"{self.tournament.title} - {self.match_date}"

from django.db import models
from django.contrib.auth.models import User

class TeamRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)

    team_logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Paid', 'Paid'),
        ],
        default='Pending'
    )

    approval_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected'),
        ],
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.team_name


class TeamPlayer(models.Model):
    team = models.ForeignKey(TeamRegistration, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=100)
    in_game_name = models.CharField(max_length=100)
    player_id = models.CharField(max_length=100)

    def str(self):
        return self.player_name


from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    in_game_name = models.CharField(max_length=100, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio=models.TextField(blank=True)

    def str(self):
        return self.user.username

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()

payment_status = models.CharField(
    max_length=20,
    default='Pending'
)

from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=100)
    game_id = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    
    player1 = models.CharField(max_length=100)
    player2 = models.CharField(max_length=100)
    player3 = models.CharField(max_length=100)
    player4 = models.CharField(max_length=100)
    player5 = models.CharField(max_length=100, blank=True, null=True)

    team_logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)


from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.name

from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ingame_name = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default-user.png')

    def _str_(self):
        return self.user.username

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()