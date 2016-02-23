from apps.api.v1.views import comment
from rest_framework import routers
from django.conf.urls import url, include


router = routers.DefaultRouter()

router.register(r'comments', comment.CommentViewSet)

urlpatterns = [
    url(r'', include(router.urls))
]
