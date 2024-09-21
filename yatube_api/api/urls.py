"""Маршруты для API."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    GroupViewSet,
    FollowViewSet,
    PostViewSet,
    CommentViewSet
)

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register('follow', FollowViewSet, basename='follow')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
