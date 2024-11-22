from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Client, ClientFile, Laptop

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'location', 'agreement_status', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('location', 'agreement_status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('location', 'agreement_status')}),
    )

class ClientFileInline(admin.TabularInline):
    model = ClientFile
    extra = 1

class LaptopInline(admin.TabularInline):
    model = Laptop
    extra = 1

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'contact_person', 'phone_number', 'registration_date')
    search_fields = ('user__username', 'company_name', 'contact_person')
    inlines = [ClientFileInline, LaptopInline]

@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'model', 'serial_number', 'status', 'client', 'assigned_date', 'return_date')
    list_filter = ('status',)
    search_fields = ('identifier', 'model', 'serial_number', 'client__user__username')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ClientFile)