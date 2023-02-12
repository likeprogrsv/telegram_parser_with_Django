from django.urls import path
from .views import show_news, TagList, PostList, PostByTag
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', show_news, name='news'),
    path('api/v1/tags/', TagList.as_view(), name='tag_list'),
    path('api/v1/posts/', PostList.as_view(), name='post_list'),
    path('api/v1/posts/<str:tag>/', PostByTag.as_view(), name='post_by_tag'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
