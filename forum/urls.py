from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # new
from django.conf.urls.static import static # new
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user-post/', views.userPost, name='user-post'),
    path('topic/<int:pk>/', views.postTopic, name='topic-detail'),
    path('search-result/', views.searchView, name='search-result'),
    path('user-dashboard/', views.userDashboard, name='user-dashboard'),
    path('upvote/', views.upvote, name='upvote'),
    path('downvote/', views.downvote, name='downvote'),
    path('blog/', views.blogListView, name='blog'),
    path('article/<slug:slug>/', views.blogDetailView, name='article-detail'),
    path('admin/', admin.site.urls),
    path('register/', include('registration.urls')),
    path('baton/', include('baton.urls')),
]

if settings.DEBUG: # this needs to be inside the if statement
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)