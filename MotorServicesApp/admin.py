from django.contrib import admin
from django import forms
#from django.contrib.auth.models import Group, User
from .models import  Area,Territory, MotorTechnician, Target, ServiceDetails, UserInfo, UserArea, EngWiseReport

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from django.core.exceptions import ValidationError
from django.conf.urls import url,include
import datetime
#from django.conf.urls.defaults import *
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.auth.decorators import user_passes_test
from django.utils.html import format_html


admin.site.site_header = "Motor Service Administration"
admin.site.site_title = "Motor Service"
admin.site.index_title = "Motor Service"


admin.site.register(Area)
admin.site.unregister(User)

class EngWiseReportAdmin(admin.ModelAdmin):
    list_display = ('show_eng_username','show_eng_full_name', 'show_firm_url', )

    def show_firm_url(self, obj):
        return format_html('<a href="http://dashboard.acigroup.info/motorservices_mobile_api/service_ratio_all_eng.php?engid=%s" target="_blank">%s</a>' % (obj.EngId, 'View Report'))

    def show_eng_username(self, obj):
        return obj.EngId.username

    def show_eng_full_name(self, obj):
        return obj.EngId.first_name+" "+obj.EngId.last_name



    def get_list_display(self, request):
        return self.list_display

    def get_queryset(self, request):
        if request.user.id == 1:
            qs = super(EngWiseReportAdmin, self).get_queryset(request)
            return qs.all()
        else:
            qs = super(EngWiseReportAdmin, self).get_queryset(request)
            return qs.filter(EngId=request.user)


    # def get_queryset(self, request):
    #     qs = super(MotorTechnicianAdmin, self).get_queryset(request)
    #     return qs.filter(user=request.user)

    # def show_firm_url(self, obj):
    #     print("===="+ self._request(self) )
    #     return format_html('<a href="http://thisisatesturl=%s" target="_blank">%s</a>' % (obj.Id, 'View Report:'))

    show_firm_url.allow_tags = False

admin.site.register(EngWiseReport, EngWiseReportAdmin)

class DummyModel(models.Model):
    class Meta:
        verbose_name_plural = 'Report'
        app_label = 'MotorServicesApp'


def my_custom_view(request):
    url='https://app.powerbi.com/view?r=eyJrIjoiMWZhNjNmYmMtNTc1Zi00N2FiLTg2YWItNzYzNmY1MThkZTA4IiwidCI6IjY1M2JkM2UxLTM2ZmYtNDM5OS1iMGFhLWY3ZTYzYTAyOTU5NyIsImMiOjEwfQ%3D%3D'
    return HttpResponseRedirect(url)

class DummyModelAdmin(admin.ModelAdmin):
    model = DummyModel

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            url('my_admin_path/', my_custom_view, name=view_name),
        ]

admin.site.register(DummyModel, DummyModelAdmin)

class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name' , 'last_name', )


class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    #filter_horizontal = ['AreaId']
    prepopulated_fields = {'username': ('first_name' , 'last_name', )}

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'password1', 'password2', 'groups','is_staff' ),
        }),
    )

    def save_model(self, request, obj, form, change):
        EngWiseReport(EngWiseReportLink="TSA Performence Report",EngId=obj).save()
        return super(UserAdmin, self).save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)

class UserAreaAdmin(admin.ModelAdmin):
    list_display = ['UserId']
    list_filter = ['UserId']
    filter_horizontal = ['AreaId']
    ordering = ['-Id']

    list_per_page = 10


admin.site.register(UserArea, UserAreaAdmin)

class TerritoryAdmin(admin.ModelAdmin):
    list_display = ('AreaId', 'Name', 'Code')
    search_fields = ['Name']
    list_filter = ['Name']
    ordering = ['-Id']
    fields = ('AreaId','Name', 'Code')
    list_per_page = 20


    def get_queryset(self, request):

        if request.user.id == 1:
            qs = super(TerritoryAdmin, self).get_queryset(request)
            return qs.all()
        else:
            qs = super(TerritoryAdmin, self).get_queryset(request)
            return qs.filter(user=request.user)


    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("user","Notes")
        kwargs['widgets'] = {'Notes': forms.Textarea}
        form = super(TerritoryAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super(TerritoryAdmin, self).save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "AreaId":
            #aList = UserArea.objects.filter(UserId=request.user).values_list('AreaId__Id', flat=True)
            kwargs["queryset"] = Area.objects.filter(Id__in=(UserArea.objects.filter(UserId=request.user).values_list('AreaId__Id', flat=True)))
        return super(TerritoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Territory, TerritoryAdmin)


class MotorTechnicianAdmin(admin.ModelAdmin):
    #list_display = ('Name', 'Designation','StaffId', 'TerritoryCode','MobileNo')
    list_display = ('Name', 'Designation', 'StaffId', 'TerritoryCode','MobileNo')
    search_fields = ['Name', 'StaffId', 'MobileNo']
    list_filter = ['StaffId', 'MobileNo']
    ordering = ['-Id']
    list_per_page = 20

    def get_queryset(self, request):
        if request.user.id == 1:
            qs = super(MotorTechnicianAdmin, self).get_queryset(request)
            return qs.all()
        else:
            qs = super(MotorTechnicianAdmin, self).get_queryset(request)
            #print("===="+str(qs))
            return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):

        obj.user = request.user
        obj.save()
        tsaUser = UserInfo.objects.filter(MotorTechnicianId=obj).first()
        if not tsaUser:
            UserInfo(UserName=str(obj.StaffId), Password=str(obj.StaffId), IsActive=1, user=request.user, MotorTechnicianId=obj).save()
        else :
            UserInfo.objects.filter(MotorTechnicianId=obj).update(UserName=str(obj.StaffId), Password=str(obj.StaffId))
        #return super(MotorTechnicianAdmin, self).save_model(request, obj, form, change)

        return obj

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("user",)
        form = super(MotorTechnicianAdmin, self).get_form(request, obj, **kwargs)
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "TerritoryCode":
            #aList = UserArea.objects.filter(UserId=request.user).values_list('AreaId__Id', flat=True)
            kwargs["queryset"] = Territory.objects.filter(user=request.user)
        return super(MotorTechnicianAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MotorTechnician, MotorTechnicianAdmin)


class TargetAdmin(admin.ModelAdmin):
    list_display = ('TechnicianCode', 'TerritoryId', 'WarrantyService', 'PostWarrantyService', 'EntryDate')
    search_fields = ['TechnicianCode', 'TerritoryId']
    list_filter = ['TechnicianCode', 'EntryDate']
    ordering = ['-Id']
    list_per_page = 20

    def get_queryset(self, request):
        # qs = super(TargetAdmin, self).get_queryset(request)
        # return qs.filter(user=request.user)

        if request.user.id == 1:
            qs = super(TargetAdmin, self).get_queryset(request)
            return qs.all()
        else:
            qs = super(TargetAdmin, self).get_queryset(request)
            return qs.filter(user=request.user)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("user",)
        form = super(TargetAdmin, self).get_form(request, obj, **kwargs)
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.id == 1:
            if db_field.name == "TechnicianCode":
                kwargs["queryset"] = MotorTechnician.objects.all()
            if db_field.name == "TerritoryId":
                kwargs["queryset"] = Territory.objects.all()
        else:
            if db_field.name == "TechnicianCode":
                kwargs["queryset"] = MotorTechnician.objects.filter(user=request.user)
            if db_field.name == "TerritoryId":
                kwargs["queryset"] = Territory.objects.filter(user=request.user)

        return super(TargetAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if request.user.id == 1:
            obj.user = request.user
            return super(TargetAdmin, self).save_model(request, obj, form, change)
        else:
            from django.contrib import messages
            dt = str(datetime.datetime.now())
            _datetime = datetime.datetime.now()
            today = datetime.date.today()
            tar = Target.objects.filter(TechnicianCode=obj.TechnicianCode, EntryDate__month=today.month)
            if tar:
                messages.set_level(request, messages.ERROR)
                #return "For this technician the target already exists in this month."
                #raise forms.ValidationError('The pools are all full.')
                messages.error(request, "For this technician the target already exists in this month.")
                return
            else:
                obj.user = request.user
                return super(TargetAdmin, self).save_model(request, obj, form, change)

admin.site.register(Target, TargetAdmin)

class ServiceDetailsAdmin(admin.ModelAdmin):
    list_display = ('TechnicianName', 'CustomerName', 'Mobile', 'HoursProvided', 'CategoryId', 'ProductId', 'CallTypeId')
    #list_display = ('CustomerName', 'Mobile')
    search_fields = [ 'CustomerName', 'Mobile']
    list_filter = ['IsVerify','CustomerName', 'UserId', 'Mobile']
    #readonly_fields = ('CustomerName',)
    ordering = ['-ServiceDetailsId']
    list_per_page = 20
    fields = ('CustomerName'
                ,'Mobile'
                ,'TractorPurchaseDate'
                ,'HoursProvided'
                ,'DateOfInstallation'
                ,'ServiceDemandDate'
                ,'ServiceStartDate'
                ,'ServiceEndDate'
                ,'ServiceIncome'
                ,'VisitDate'
                ,'UserId'
                ,'CategoryId'
                ,'ProductId'
                ,'CallTypeId'
                ,'IsVerify')

    def TechnicianName(self, obj):
        staffId = UserInfo.objects.filter(UserName=obj.UserId).values('UserName').first()
        result = MotorTechnician.objects.filter(StaffId=staffId['UserName']).values('Name').first()

        return result.get('Name')

    TechnicianName.short_description = 'Technician'

    def get_queryset(self, request):
        #print("==="+str(request.user.id))
        if request.user.id == 1:
            qs = super(ServiceDetailsAdmin, self).get_queryset(request)
            return qs.all()
        else:
            qs = super(ServiceDetailsAdmin, self).get_queryset(request)
            return qs.filter(SupervisorCode=request.user)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "UserId":
            kwargs["queryset"] = UserInfo.objects.filter(UserName__in=(MotorTechnician.objects.filter(user=request.user).values('StaffId')))
        # if db_field.name == "TerritoryId":
        #     kwargs["queryset"] = ServiceDetails.objects.filter(SupervisorCode=request.user)
        return super(ServiceDetailsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("SupervisorCode",)
        return super(ServiceDetailsAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(ServiceDetails, ServiceDetailsAdmin)


# def my_view(request):
#     return HttpResponse("Hello!")
#
# def get_admin_urls(urls):
#     def get_urls():
#         my_urls = [
#             url(r'^my_view/$', admin.site.admin_view(my_view))
#         ]
#         return my_urls + urls
#     return get_urls
#
# admin_urls = get_admin_urls(admin.site.get_urls())
# admin.site.get_urls = admin_urls


# def get_admin_urls(urls):
#     def get_urls():
#         my_urls =  include('',
#            url(r'^$', AllReportForEng,name='home'),
#         )
#         return my_urls + urls
#     return get_urls

# @admin.site.register_view('hello', urlname='custom_hello', name='Greets you with a hello')
# def custom_hello(request):
#     return render(request, 'myapp/hello.html', {})
#
# @admin.site.register_view('Report')
# def my_view(request):
#     return

# class CustomAdminSite(admin.AdminSite):
#     def get_urls(self):
#         urls = super(CustomAdminSite, self).get_urls()
#         custom_urls = [
#             url(r'report^$', self.admin_view(AllReportForEng), name="report"),
#         ]
#         return urls + custom_urls
#
# admin.site.register(CustomAdminSite)
#admin.autodiscover()

# admin_urls = get_admin_urls(admin.site.get_urls())
# admin.site.get_urls = admin_urls

# class MyModelAdmin(admin.ModelAdmin):
#     def get_urls(self):
#         urls = super(MyModelAdmin, self).get_urls()
#         my_urls = include('',
#             (r'^my_view/$', AllReportForEng)
#         )
#         return my_urls + urls
#
#     def my_view(self, request):
#         # custom view which should return an HttpResponse
#         pass
#
# admin.autodiscover()
# admin.site.register(MyModelAdmin)
#admin_urls = get_admin_urls(admin.site.get_urls())
#admin.site.get_urls = admin_urls


