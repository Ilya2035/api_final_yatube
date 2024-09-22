"""Маршруты для API."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    GroupViewSet,
    FollowViewSet,
    PostViewSet,
    CommentViewSet
)

version_n1_router = DefaultRouter()
version_n1_router.register('posts', PostViewSet, basename='posts')
version_n1_router.register('groups', GroupViewSet, basename='groups')
version_n1_router.register('follow', FollowViewSet, basename='follow')
version_n1_router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(version_n1_router.urls)),
]
