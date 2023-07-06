from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import pandas as pd

from COC_API import COC_API
from Members_Managment.my_models import Member
from Raid_Managment.my_models import Raid

# Create your views here.

def viewattacks(request):

    if "raid_info" not in request.session:
        raid_info, raid_attacks_info = Raid.get_last_raid_info(request.session["clan_tag"])

        request.session["raid_info"] = raid_info
        request.session["raid_attacks_info"] = raid_attacks_info.to_dict("records")

    return render(request, "ViewAttacks.html", {"raid_info": request.session["raid_info"], "raid_attacks_info": request.session["raid_attacks_info"]})


def refresh_raid_info(request):
    raid_info, raid_attacks_info = Raid.get_last_raid_info(request.session["clan_tag"])

    request.session["raid_info"] = raid_info
    request.session["raid_attacks_info"] = raid_attacks_info.to_dict("records")


    return JsonResponse({"status": "success"})