from django.contrib import admin
from .models import CustomUser, HotelRoom
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('patronymic', 'phone_number', 'registration_address', 'gender', 'role', 'is_banned')}),
    )
    

@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status', 'price')
