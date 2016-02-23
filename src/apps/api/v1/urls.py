from apps.api.v1 import views
from rest_framework import routers
from django.conf.urls import url, include


router = routers.DefaultRouter()

router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    url(r'', include(router.urls))
]
