from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
import drinks.api.urls.drink_urls as drink_urls
import drinks.api.urls.user_urls as user_urls
import drinks.api.urls.votes_urls as vote_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(drink_urls)), 
    path('api/', include(user_urls)),
    path('api/', include(vote_urls)), 
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
