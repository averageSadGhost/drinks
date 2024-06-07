from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from drinks import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drinks/', views.drink_list, name='drink_list'),
    path('drinks/<int:id>/', views.drink_detail, name='drink_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('users/<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('users/', views.get_all_users, name='get_all_users'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
