from django.shortcuts import render
from django.db import connection, connections
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
import re
import csv
import requests
import time
import sys
from .models import *
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import urllib.request
from django.views.generic import FormView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from django.http import HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
#from rest_framework.response import Response
import numpy as np
import datetime
from decimal import Decimal
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import F
from collections import defaultdict
SESSION_ID = "ABC"


# Create your views here.

def Login(request):
    if request.method == 'GET':
        if 'UserID' not in request.session:
            return render(request, 'MotorServicesApp/Login.html')
        else:
            UserID = request.session['UserID']
            return render(request, 'MotorServicesApp/Login.html')
    if request.method == 'POST':
        UserName = request.POST.get('UserName')
        Password = request.POST.get('Password')
        userObj = UserManager.objects.filter(UserName=UserName, Password=Password).first()


        if userObj is not None:
            if Password == str(userObj.Password):
                #request.session['uid'] = str(userObj.Id)
                request.session['UserID'] = str(userObj.UserID)                
                request.session['UserName'] = str(userObj.UserName)
                request.session['Password'] = Password
                #request.session['DisplayName'] = DisplayName
                #request.session['Status'] = Status #str(userObj.DepartmentId.DepartmentName)
                #request.session['Department'] = str(userObj.DepartmentId.Id)

                if not request.session.session_key:
                    request.session.save()
                global SESSION_ID
                print(request.session['UserName'])

                return HttpResponseRedirect('Home')
            else:
                return render(request, 'MotorServicesApp/Login.html',{'message':'UserName Password mismass'})
        else:
            return render(request, 'MotorServicesApp/Login.html',{'message':'UserName Password mismass'})


    return render(request, 'MotorServicesApp/Login.html')

#@login_required(login_url='/')
def Home(request):
    if 'UserID' not in request.session:
        return render(request, 'MotorServicesApp/Login.html')
    else:
        context = {'PageTitle': 'Home'}
        return render(request, 'MotorServicesApp/Home.html',context)

def TerritoryReport(request):
    if 'UserID' not in request.session:
        return render(request, 'MotorServicesApp/Login.html')
    else:
        userId = request.session['UserID']
        AreaName = AreaNew.objects.filter(pk=int(userId)).first()
        ttyList = TerritoryNew.objects.filter(AreaName=AreaName).values('TerritoryName', 'AreaName__Name')
        print("===="+str(ttyList))
        context = {'PageTitle': 'Home', 'ttyList': ttyList}
        return render(request, 'MotorServicesApp/TerritoryReport.html',context)

def AddNewTerritory(request):
    if 'UserID' not in request.session:
        return render(request, 'MotorServicesApp/Login.html')
    else:
        userId = request.session['UserID']
        AreaName = AreaNew.objects.filter(pk=int(userId)).first()
        ttyList = TerritoryNew.objects.filter(AreaName=AreaName).values('TerritoryName', 'AreaName__Name')
        print("===="+str(ttyList))
        context = {'PageTitle': 'Home', 'ttyList': ttyList}
        return render(request, 'MotorServicesApp/AddTerritory.html',context)

def territory_create(request, template_name='MotorServicesApp/AddTerritory.html'):
    if 'UserID' not in request.session:
        return render(request, 'MotorServicesApp/Login.html')
    else:
        form = TerritoryForm(request.POST or None)
        if form.is_valid():
            form.save()
        return redirect('MotorServicesApp/TerritoryReport.html')
        return render(request, template_name, {'form':form})

def TechnicianReport(request):
    if 'UserID' not in request.session:
        return render(request, 'MotorServicesApp/Login.html')
    else:
        userId = request.session['UserID']
        user = UserManager.objects.filter(pk=int(userId)).first()
        tecList = Technician.objects.filter(EntryBy=user).values('TechnicianName','StaffID', 'Designation')
        print("===="+str(tecList))
        context = {'PageTitle': 'Home', 'tecList': tecList}
        return render(request, 'MotorServicesApp/TechnicianReport.html',context)

def AddNewTechnician(request):
    if 'UserID' not in request.session:
        return render(request, 'MotorServicesApp/Login.html')
    else:
        userId = request.session['UserID']
        AreaName = AreaNew.objects.filter(pk=int(userId)).first()
        ttyList = TerritoryNew.objects.filter(AreaName=AreaName).values('TerritoryName', 'AreaName__Name')
        print("===="+str(ttyList))
        context = {'PageTitle': 'Home', 'ttyList': ttyList}
        return render(request, 'MotorServicesApp/AddTechnician.html',context)
        
def Logout(self):
    if 'UserID' not in self.session:
        return HttpResponseRedirect('/')
    else:
        self.session.flush()
        self.session.clear()
        del self.session
        return HttpResponseRedirect('/')
