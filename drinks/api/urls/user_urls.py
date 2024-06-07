from django.urls import path
from ..views import user_views as views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('users/<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('users/', views.get_all_users, name='get_all_users'),
]
