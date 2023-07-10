from django.urls import path

from . import views

urlpatterns = [
    path("Config/Constantes", views.ViewConstantes, name="Constantes"),
    path("Config/Constantes/<int:id_delete>", views.ViewConstantes, name="Constantes"),
    path("Config/Constantes/<str:msg_error>", views.ViewConstantes, name="Constantes")
]