from django.contrib import admin
from django import forms
#from django.contrib.auth.models import Group, User
from .models import  Area,Territory, MotorTechnician, Target, ServiceDetails, UserInfo, UserArea

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User





admin.site.site_header = "Motor Service Administration"
admin.site.site_title = "Motor Service"
admin.site.index_title = "Motor Service"


admin.site.register(Area)
admin.site.unregister(User)

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
admin.site.register(User, UserAdmin)


class TerritoryForm(forms.ModelForm):
    AreaId = forms.ModelChoiceField(queryset=Area.objects.all(),empty_label="Select an Area",label='Area')

    class Meta:
        model = Territory
        exclude = ['user','Notes']


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
    form =TerritoryForm

    def get_queryset(self, request):
        qs = super(TerritoryAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)

    def get_form(self, request, obj=None, **kwargs):
        #self.exclude = ("user","Notes")

        kwargs['widgets'] = {'Notes': forms.Textarea }

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
        qs = super(MotorTechnicianAdmin, self).get_queryset(request)
        #print("===="+str(qs))
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        UserInfo(UserName=str(obj.StaffId), Password=str(obj.StaffId), IsActive=1, user=request.user).save()
        obj.user = request.user
        return super(MotorTechnicianAdmin, self).save_model(request, obj, form, change)

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
        qs = super(TargetAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("user",)
        form = super(TargetAdmin, self).get_form(request, obj, **kwargs)
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "TechnicianCode":
            kwargs["queryset"] = MotorTechnician.objects.filter(user=request.user)
        if db_field.name == "TerritoryId":
            kwargs["queryset"] = Territory.objects.filter(user=request.user)

        return super(TargetAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super(TargetAdmin, self).save_model(request, obj, form, change)

admin.site.register(Target, TargetAdmin)

class ServiceDetailsAdmin(admin.ModelAdmin):
    list_display = ('CustomerName', 'Mobile', 'HoursProvided', 'CategoryId', 'ProductId', 'CallTypeId')
    #list_display = ('CustomerName', 'Mobile')
    search_fields = ['CustomerName', 'Mobile']
    list_filter = ['IsVerify','CustomerName', 'Mobile']
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



    def get_queryset(self, request):
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

