from django_select2.views import AutoResponseView
from core.models import Goal


class IdeaChainedView(AutoResponseView):
    def get_queryset(self):
        goal_id = self.request.GET.get('goal_id', False)
        queryset = self.queryset

        if goal_id:
            queryset = Goal.objects.get(pk=goal_id)
            queryset = queryset.goal_ideas.all()

        return self.widget.filter_queryset(self.term, queryset)
