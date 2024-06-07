from django.urls import path
from ..views import vote_views as views

urlpatterns = [
    path('drinks/<int:drink_id>/votes/', views.get_votes_for_post, name='get_votes_for_post'),
    path('drinks/<int:drink_id>/upvote/', views.upvote, name='upvote'),
    path('drinks/<int:drink_id>/downvote/', views.downvote, name='downvote'),
]
