from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("Members/View", views.members, name="members"),
    path("Members/Refresh", views.refresh_info, name="update_members"),
    path("Members/Edit/Cel_Comment", views.editar_cel_coment_miembro, name="editar_cel_coment_miembro"),
    path("Members/History", views.members_history, name="members_history"),
    path("Members/History/Get", views.get_member_history, name="get_member_history"),
    path("Members/History/SaveChanges", views.save_changes_history_member, name="save_changes_history_member")
]