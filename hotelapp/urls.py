from django.urls import path
from .views import login_view, index, register_view, logout_view, change_password, add_user, edit_user, user_list, unban_user, ban_user, contacts, aboutUs
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('aboutUs/', aboutUs, name='aboutUs'),
    path('change-password/', change_password, name='change_password'),
    path('add_user/', add_user, name='add_user'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('user_list/', user_list, name='user_list'), 
    path('ban/<int:user_id>/', ban_user, name='ban_user'),
    path('user/<int:user_id>/unban/', unban_user, name='unban_user'),


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
