from django.urls import path
from ..views import drink_views as views

urlpatterns = [
    path('drinks/<int:id>/', views.drink_detail, name='drink_detail'),
    path('drinks/', views.drink_list, name='drink_list'),
    path('drinks/search/', views.search_drinks, name='search_drinks'),
]
