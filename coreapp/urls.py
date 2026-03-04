from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('tournament/', views.tournament, name='tournament'),
    path('join/<int:tournament_id>/', views.join_tournament, name='join_tournament'),
    path('my-tournaments/', views.my_tournaments, name='my_tournaments'),

    path('rulebook/', views.rulebook, name='rulebook'),
    path('match-schedule/', views.match_schedule, name='match_schedule'),

    path('team_register/<int:tournament_id>/', views.team_register, name='team_register'),

    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),

    path('payment/<int:registration_id>/', views.payment_page, name='payment'),
    path('payment-success/<int:registration_id>/', views.payment_success, name='payment_success'),

    path('guidelines/', views.rulebook2, name='rulebook2'),
    
    path('all_team_entries/', views.all_team_entries, name='all_team_entries'),
    
    path('contact/', views.contact, name='contact'),

    path('match-results/', views.match_results, name='match_results'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
