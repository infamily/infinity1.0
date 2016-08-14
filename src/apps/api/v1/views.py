from django.utils.translation import ugettext as _
from django.db.models import Q
from .serializers import GoalSerializer, IdeaSerializer, PlanSerializer
from rest_framework import viewsets, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Goal, Idea, Plan
from .pagination_classes import StandardResultsSetPagination
from django.core.paginator import Paginator as DjangoPaginator
from django.contrib.contenttypes.models import ContentType
from core.models import Translation
from core.models import Language
from rest_framework import permissions


class BaseViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        response = super(BaseViewSet, self).list(request, *args, **kwargs)

        models_map = {
            Goal: {
                'description': _('Where people share and discuss the world\'s issues.'),
                'types': {
                    'project': _('Projects'),
                    'solution': _('Solutions'),
                    'problem': _('Problems'),
                    'current': _('Problem')
                }
            },
            Idea: {
                'description': _('Where people share and discuss ideas how to solve them.'),
                'types': {
                    'project': _('Projects'),
                    'solution': _('Solutions'),
                    'problem': _('Problems'),
                    'current': _('Solution')
                }
            },
            Plan: {
                'description': _('Where people start initiatives to realize them.'),
                'types': {
                    'project': _('Projects'),
                    'solution': _('Solutions'),
                    'problem': _('Problems'),
                    'current': _('Project')
                }
            }
        }

        response.data.update(models_map[self.queryset.model])

        return response

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        qs = super(BaseViewSet, self).get_queryset()
        # language_id = self.request.query_params.get('language', None)
        content_type = ContentType.objects.get_for_model(qs.model)

        language = Language.objects.get(language_code=self.request.LANGUAGE_CODE)

        translations = Translation.objects.filter(content_type=content_type, language=language)

        qs = qs.filter(id__in=translations.values_list('object_id', flat=True))

        query = Q(personal=False)

        if self.request.user.is_authenticated():
            query |= Q(personal=True, user=self.request.user) | Q(personal=True, sharewith=self.request.user)

        qs = qs.filter(query)
        qs = qs.order_by('-commented_at')
        qs = qs.distinct()

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
