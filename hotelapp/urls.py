from django.urls import path
from .views import login_view, index, register_view, logout_view, change_password
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('', index, name='index'),
    path('change-password/', change_password, name='change_password'),


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
