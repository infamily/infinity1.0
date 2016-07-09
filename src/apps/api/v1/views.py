from api.v1.serializers import GoalSerializer, IdeaSerializer
from rest_framework import viewsets, generics
from core.models import Goal, Idea
from .pagination_classes import StandardResultsSetPagination


class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Idea.objects.all()
        language_id = self.request.query_params.get('language', None)

        if language_id is not None:
            queryset = queryset.filter(language=language_id)

        return queryset


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
