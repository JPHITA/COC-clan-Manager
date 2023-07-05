from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from COC_API import COC_API

# Create your views here.

def viewattacks(request):

    

    return render(request, "ViewAttacks.html")