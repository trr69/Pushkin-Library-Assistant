from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('app.news_app.urls')),
    path('dosai/', include('app.chatbot_app.urls')),
    path('events/', include('app.events_app.urls')),
    path('courses/', include('app.courses_app.urls')),
    path('search_books/', include("app.book_search_app.urls")),
    path('', include('core.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)