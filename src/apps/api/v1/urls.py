from django.conf.urls import url, include
from rest_framework import routers
from api.v1 import views

router = routers.SimpleRouter()
router.register(r'goals', views.GoalViewSet, base_name='goal-list')
router.register(r'ideas', views.IdeaViewSet, base_name='idea-list')
router.register(r'plans', views.PlanViewSet, base_name='plan-list')

urlpatterns = [
    url(r'^', include(router.urls))
]
