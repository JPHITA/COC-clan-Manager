from django.urls import path

from . import views

urlpatterns = [
    path("ClanWar/ViewAttacks", views.viewattacks, name="ViewAtacks"),
    path("ClanWar/RefreshClanWarInfo", views.refresh_clanwar_info, name="RefreshClanWarInfo")
]