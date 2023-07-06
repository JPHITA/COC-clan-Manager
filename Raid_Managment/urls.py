from django.urls import path

from . import views

urlpatterns = [
    path("Raid/ViewAttacks", views.viewattacks, name="ViewAtacks"),
    path("Raid/RefreshRaidInfo", views.refresh_raid_info, name="RefreshRaidInfo")
]