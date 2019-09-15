from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import UserManager, Status, AreaNew

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name' , 'last_name', )


class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    prepopulated_fields = {'username': ('first_name' , 'last_name', )}

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'password1', 'password2', 'groups','is_staff' ),
        }),
    )
admin.site.unregister(User)
admin.site.register(User, UserAdmin)



# Register your models here.

admin.site.site_header = 'Motor Service Administration'
admin.site.site_title = "Motor Service"
admin.site.index_title = "Motor Service"

# class UserManagerAdmin(admin.ModelAdmin):
#     list_display = [ 'UserName', 'Password', 'AccessLevel', 'Status', 'DisplayName']
#     search_fields = [ 'UserName', 'DisplayName']
#     list_filter = ['DisplayName', 'UserName']
#     list_per_page = 20
#
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "AccessLevel":
#             kwargs["queryset"] = AreaNew.objects.all()
#         if db_field.name == "Status":
#             kwargs["queryset"] = Status.objects.all()
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
#
# admin.site.register(UserManager, UserManagerAdmin)

#admin.site.unregister(Group)
#admin.site.unregister(User)



