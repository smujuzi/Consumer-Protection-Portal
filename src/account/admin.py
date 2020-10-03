from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account




class AccountAdministrator(UserAdmin):
    list_display = (
        'email', 'full_names', 'phone_number', 'address', 'role', 'date_joined', 'last_login', 'image', 'is_admin',
        'is_staff')
    search_fields = ('email', 'full_names',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('full_names',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_names', 'role', 'image')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Contact info', {'fields': ('phone_number', 'address')}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = ((None, {'fields': ('email', 'password1', 'password2')}),
                     ('Personal info', {'fields': ('full_names', 'role', 'image')}),
                     ('Contact info', {'fields': ('phone_number', 'address')}),
                     ('Permissions',
                      {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}))


admin.site.register(Account, AccountAdministrator)
