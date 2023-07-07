from django.shortcuts import render, redirect

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

        return render(request, "ResumenClanes.html", {"state": "in_war", "CWL_clans_summary": CWL_clans_summary})


def GuerraEspecifica(request):
    pass


def Refresh(request):
    request.session["CWL_info"] = COC_API.get_CWL_info(request.session["clan_tag"])

    return redirect("")