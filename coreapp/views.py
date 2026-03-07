from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError

from .models import (
    Tournament,
    TournamentJoin,
    MatchSchedule,
    TeamRegistration,
    TeamPlayer,
    UserProfile
)

# ================= HOME =================

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# ================= AUTH =================

def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            return render(request, "signup.html", {"error": "User already exists"})

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )
        user.save()
        return redirect("login")

    return render(request, 'signup.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect("tournament")
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'login.html')


# ================= TOURNAMENT =================

@login_required
def tournament(request):
    tournaments = Tournament.objects.all()

    registered_tournaments = TeamRegistration.objects.filter(
        user=request.user
    ).values_list('tournament_id', flat=True)

    return render(request, 'tournament.html', {
        'tournaments': tournaments,
        'registered_tournaments': registered_tournaments
    })


@login_required
def join_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)

    TournamentJoin.objects.get_or_create(
        user=request.user,
        tournament=tournament
    )

    return redirect('team_register', tournament_id=tournament.id)


@login_required
def my_tournaments(request):
    joins = TournamentJoin.objects.filter(
        user=request.user
    ).select_related('tournament')

    return render(request, 'my_tournaments.html', {'joins': joins})


@login_required
def rulebook(request):
    return render(request, "rulebook.html")

# ================= MATCH =================

@login_required
def match_schedule(request):
    joined = TournamentJoin.objects.filter(
        user=request.user
    ).values_list('tournament', flat=True)

    schedules = MatchSchedule.objects.filter(
        tournament__in=joined
    )

    return render(request, 'match_schedule.html', {'schedules': schedules})

# ================= TEAM REGISTRATION =================
@login_required
def team_register(request, tournament_id):

    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.method == "POST":

        team_name = request.POST.get("team_name")

        # Create team registration
        team = TeamRegistration.objects.create(
            user=request.user,
            tournament=tournament,
            team_name=team_name
        )

        # Loop for players
        for i in range(1, 5):
            name = request.POST.get(f"player{i}_name")
            ign = request.POST.get(f"player{i}_ign")
            pid = request.POST.get(f"player{i}_id")

            if name and ign and pid:
                TeamPlayer.objects.create(
                    team=team,
                    player_name=name,
                    in_game_name=ign,
                    player_id=pid
                )

        return redirect('payment', registration_id=team.id)

    return render(request, 'team_register.html', {
        'tournament': tournament
    })

# ================= DASHBOARD =================

@login_required
def dashboard(request):
    teams = TeamRegistration.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'teams': teams})

# ================= PROFILE =================

@login_required
def profile(request):
    profile = request.user.userprofile
    registrations = request.user.teamregistration_set.all()

    return render(request, 'profile.html', {
        'profile': profile,
        'registrations': registrations
    })

# ================= PAYMENT =================

@login_required
def payment_page(request, registration_id):
    registration = get_object_or_404(
        TeamRegistration,
        id=registration_id,
        user=request.user
    )

    return render(request, 'payment.html', {'registration': registration})


@login_required
def payment_success(request, registration_id):
    registration = get_object_or_404(
        TeamRegistration,
        id=registration_id,
        user=request.user
    )

    registration.payment_status = "Paid"
    registration.save()

    messages.success(request, "Tournament registration successful!")

    return redirect('tournament')

def rulebook2(request):
    return render(request, 'rulebook2.html')

def all_team_entries(request):
    teams = TeamRegistration.objects.filter(approval_status="Approved")

    return render(request, "all_team_entries.html", {
        "teams": teams
    })


from django.shortcuts import render
from django.contrib import messages
from .models import ContactMessage

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        messages.success(
            request,
            "Thanks for your message. The Game Desk org will  Answer your message."
        )

        return redirect("contact")

    return render(request, "contact.html")

def match_results(request):
    return render(request, 'match_results.html')
