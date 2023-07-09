from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from COC_API import COC_API
from CWL_Managment.my_models import CWL


# Create your views here.

def ResumenClanes(request):

    if "CWL_info" not in request.session:
        request.session["CWL_info"] = COC_API.get_CWL_info(request.session["clan_tag"])
    
    if request.session["CWL_info"]["state"] != "inWar":
        return render(request, "ResumenClanes.html", {"state": "not_in_war"})
    
    else:
        CWL_clans_summary = CWL.ResumenClanes(request.session["CWL_info"]["clans"])
        ronda_disp = [ r["warTags"][0] != "#0" for r in request.session["CWL_info"]["rounds"] ]

        return render(request, "ResumenClanes.html", {"state": "in_war", "CWL_clans_summary": CWL_clans_summary, "ronda_disp": ronda_disp})


def GuerraEspecifica(request):
    return HttpResponse("<h1>No permitido</h1>")
    # el mapposition no tiene sentido

    if request.session["CWL_info"]["state"] != "inWar":
        return render(request, "GuerraEspecifica.html", {"state": "not_in_war"})

    else:
        ronda_disp = [ r["warTags"][0] != "#0" for r in request.session["CWL_info"]["rounds"] ]

        return render(request, "GuerraEspecifica.html", {"state": "in_war", "ronda_disp": ronda_disp})
    

def Info_GuerraEspecifica(request, round):
    
    war_tags =  request.session["CWL_info"]["rounds"][round]["warTags"]
    CWL_ataques_faltantes = CWL.Info_GuerraEspecifica(request.session["clan_tag"], war_tags)

    return JsonResponse({"state": "ok", "CWL_ataques_faltantes": CWL_ataques_faltantes})


def Refresh(request):
    request.session["CWL_info"] = COC_API.get_CWL_info(request.session["clan_tag"])

    return redirect("/CWL/ClansSummary")