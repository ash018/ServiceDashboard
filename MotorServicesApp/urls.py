"""MotorServices URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from django.conf.urls import url
from .views import *
from . import views
#from . import qcweightmentview
#from . import productionview
#from . import ajaxresponseview


urlpatterns = [
    url(r'^$', views.Login, name='Login'),
    url(r'^Home', views.Home, name='Home'),
    url(r'^TerritoryReport', views.TerritoryReport, name='TerritoryReport'),
    url(r'^AddNewTerritory', views.AddNewTerritory, name='AddNewTerritory'),
    url(r'^TechnicianReport', views.TechnicianReport, name='TechnicianReport'),
    url(r'^AddNewTechnician', views.AddNewTerritory, name='AddNewTechnician'),
    url(r'^Logout', views.Logout, name='Logout'),
]

