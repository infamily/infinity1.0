from django_select2.views import AutoResponseView
from core.models import Goal
from core.models import Idea


class GoalChainedView(AutoResponseView):
    def get_queryset(self):
        idea_id = self.request.GET.get('idea_id', False)
        queryset = self.queryset

        if idea_id:
            queryset = Idea.objects.get(pk=idea_id)
            queryset = queryset.goal.all()

        return self.widget.filter_queryset(self.term, queryset)


class IdeaChainedView(AutoResponseView):
    def get_queryset(self):
        goal_id = self.request.GET.get('goal_id', False)
        queryset = self.queryset

        if goal_id:
            queryset = Goal.objects.get(pk=goal_id)
            queryset = queryset.goal_ideas.all()

        return self.widget.filter_queryset(self.term, queryset)
