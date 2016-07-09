from api.v1.serializers import GoalSerializer, IdeaSerializer, PlanSerializer
from rest_framework import viewsets, generics
from core.models import Goal, Idea, Plan
from .pagination_classes import StandardResultsSetPagination


class IdeaViewSet(viewsets.ModelViewSet):
    serializer_class = IdeaSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Idea.objects.all()
        language_id = self.request.query_params.get('language', None)

        if language_id is not None:
            queryset = queryset.filter(language=language_id)

        return queryset


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Goal.objects.all()
        language_id = self.request.query_params.get('language', None)

        if language_id is not None:
            queryset = queryset.filter(language=language_id)

        return queryset


class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Plan.objects.all()
        language_id = self.request.query_params.get('language', None)

        if language_id is not None:
            queryset = queryset.filter(language=language_id)

        return queryset
