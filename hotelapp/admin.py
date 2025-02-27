from django.contrib import admin
from .models import CustomUser, HotelRoom

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_banned', 'last_login')
    list_filter = ('is_banned', 'role')
    search_fields = ('username', 'email', 'phone_number')
    actions = ['unban_users']

    def unban_users(self, request, queryset):
        queryset.update(is_banned=False)
        self.message_user(request, "Выбранные пользователи разблокированы.")


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status', 'price')

admin.site.register(CustomUser, CustomUserAdmin)  # ✅ Оставляем только это
