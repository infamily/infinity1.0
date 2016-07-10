from django.db.models import Q
from api.v1.serializers import GoalSerializer, IdeaSerializer, PlanSerializer
from rest_framework import viewsets, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Goal, Idea, Plan
from .pagination_classes import StandardResultsSetPagination
from django.core.paginator import Paginator as DjangoPaginator


class BaseViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        qs = super(BaseViewSet, self).get_queryset()
        language_id = self.request.query_params.get('language', None)

        query = Q(personal=False)
        if self.request.user.is_authenticated():
            query |= Q(personal=True, user=self.request.user) | Q(personal=True, sharewith=self.request.user)

        if language_id is not None:
            query &= Q(language=language_id)

        # TODO: Should be distinct here
        # but distinct does not work properly with pagination
        qs = qs.filter(query)

        return qs


class IdeaViewSet(BaseViewSet):
    serializer_class = IdeaSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Idea.objects.all()


class GoalViewSet(BaseViewSet):
    serializer_class = GoalSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Goal.objects.all()


class PlanViewSet(BaseViewSet):
    serializer_class = PlanSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Plan.objects.all()
