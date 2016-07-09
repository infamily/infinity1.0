from django.conf.urls import url, include
from rest_framework import routers
from api.v1 import views

router = routers.SimpleRouter()
router.register(r'goals', views.GoalViewSet, base_name='goals-list')

urlpatterns = [
    url(r'^', include(router.urls))
]
