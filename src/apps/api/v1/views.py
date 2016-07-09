from api.v1.serializers import GoalSerializer
from rest_framework import viewsets, generics
from core.models import Goal
from .pagination_classes import StandardResultsSetPagination


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Goal.objects.all()
        language_id = self.request.query_params.get('language', None)

        if language_id is not None:
            queryset = queryset.filter(language=language_id)

        return queryset
