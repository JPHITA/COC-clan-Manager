from django.urls import path

from . import views

urlpatterns = [
    path("CWL/ClansSummary", views.ResumenClanes, name="ResumenClanes"),
    path("CWL/SpecificWar", views.GuerraEspecifica, name="GuerraEspecifica"),
    path("CWL/InfoWar/<int:round>", views.Info_GuerraEspecifica, name="GuerraEspecifica"),
    path("CWL/Refresh", views.Refresh, name="Refresh")
]