"""
Main url patterns for API versioning
"""

from django.conf.urls import include, url

urlpatterns = [
    url(r'v1/', include('apps.api.v1.urls', namespace='v1')),
    url(r'^docs/', include('rest_framework_docs.urls')),
]
