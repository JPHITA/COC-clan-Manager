from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from Members_Managment.my_models import Member
from COC_API import COC_API
from datetime import datetime

def index(request):
    request.session["clan_tag"] = "#L0PGJP0Y"

    if "clan_info" not in request.session:
        clan_info, clan_members = COC_API.get_clan_info_members(request.session["clan_tag"])

        # guardar en la session la informacion del clan y los miembros
        request.session["clan_info"] = clan_info
        request.session["clan_members"] = clan_members

    return render(request, "index.html", {"clan_info": request.session["clan_info"]})

def refresh_info(request):
    # se obtiene la informacion de los miembros del clan
    clan_info, clan_members = COC_API.get_clan_info_members(request.session["clan_tag"])

    # guardar en la session la informacion del clan y los miembros
    request.session["clan_info"] = clan_info
    request.session["clan_members"] = clan_members

    return redirect("/Members/View")

@csrf_protect
def members(request):
    # verificar si se actualizo el nombre o el rol de algun miembro    
    Member.verify_modified_fields(request.session["clan_tag"], request.session["clan_members"])

    # verificar si hay nuevos miembros o miembros que se fueron
    Member.verify_new_and_leaving_members(request.session["clan_tag"], request.session["clan_members"])

    members = Member.get_active_membersBD(request.session["clan_tag"])
    
    return render(request, "members.html", {"members": members.to_dict("records")})



def editar_cel_coment_miembro(request):
    tag = request.POST["tag"]
    cel = request.POST["cel"]
    coment = request.POST["comments"]


    member = Member()
    member.tag = tag
    member.cel = cel if cel != "" else None
    member.comments = coment if coment != "" else None
    member.date_updated = datetime.now().strftime('%Y-%m-%d')

    member.update(campos=["cel", "comments", "date_updated"])

    return redirect("/Members/View")


@csrf_protect
def members_history(request):

    return render(request, "members_history.html")


@csrf_protect
def get_member_history(request):
    tag = request.POST["tag"]

    status, member = Member.get_historical_memberBD(tag)

    return JsonResponse({"status": status, "member": member})


@csrf_protect
def save_changes_history_member(request):
    member = Member()
    member.tag = request.POST["tag"]
    member.cel = request.POST["cel"]
    member.comments = request.POST["comments"]
    member.date_updated = datetime.now().strftime('%Y-%m-%d')

    status = "ok" if member.update(campos=["cel", "comments", "date_updated"]) == True else "error"

    return JsonResponse({"status": status})