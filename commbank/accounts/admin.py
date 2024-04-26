from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserInfo, Account, Transaction, BranchInfo

class CustomUserAdmin(BaseUserAdmin):
    ordering = ['client_id']  # Update the ordering to use 'client_id'
    fieldsets = (
        (None, {'fields': ('client_id', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('client_id', 'password1', 'password2'),
        }),
    )
    list_display = ('client_id', 'is_staff')
    search_fields = ('client_id',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(Transaction)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserInfo)
admin.site.register(Account)
admin.site.register(BranchInfo)




# ID : 234567   Password : hello098
# ID : 123456   Password : hello786