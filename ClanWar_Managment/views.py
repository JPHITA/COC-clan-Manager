from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from ClanWar_Managment.my_models import ClanWar
# Create your views here.

def viewattacks(request):
    
    if "clanwar_info" not in request.session:
        success, msg, clanwar_info, clanwar_attacks_info = ClanWar.get_ClanWar_info(request.session["clan_tag"])

        if not success:
            return redirect("/Config/Constantes/"+msg)

        request.session["clanwar_info"] = clanwar_info
        request.session["clanwar_attacks_info"] = clanwar_attacks_info

    return render(request, "ViewClanWarAttacks.html", {"clanwar_info": request.session["clanwar_info"], "clanwar_attacks_info": request.session["clanwar_attacks_info"]})


def refresh_clanwar_info(request):
    success, msg, clanwar_info, clanwar_attacks_info = ClanWar.get_ClanWar_info(request.session["clan_tag"])

    if not success:
        return redirect("/Config/Constantes/"+msg)

    request.session["clanwar_info"] = clanwar_info
    request.session["clanwar_attacks_info"] = clanwar_attacks_info

    return redirect("/ClanWar/ViewAttacks")