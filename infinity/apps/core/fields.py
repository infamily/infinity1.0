from django_select2.fields import AutoModelSelect2Field
from django_select2.fields import AutoModelSelect2MultipleField

from .models import Definition
from .models import Type
from .models import Goal
from .models import Idea
from .models import Language
from users.models import User


class TypeChoiceField(AutoModelSelect2Field):
    queryset = Type.objects

    def get_results(self, request, term, page, context):
        types = Type.objects.all()
        s2_results = [(n.id, n.name, {}) for n in types]
        return ('nil', False, s2_results)


class DefinitionChoiceField(AutoModelSelect2Field):
    queryset = Definition.objects.all()
    search_fields = ['name__icontains']


class GoalChoiceField(AutoModelSelect2Field):
    queryset = Goal.objects

    def get_results(self, request, term, page, context):
        idea = request.GET.get('idea', '')
        if idea:
            goals = Idea.objects.get(pk=idea).goal.all()
        else:
            # If idea not present show all goals
            goals = Goal.objects.all()
        s2_results = [(n.id, n.name, {}) for n in goals]
        return ('nil', False, s2_results)


class GoalChoiceFieldMultiple(AutoModelSelect2MultipleField):
    queryset = Goal.objects

    def get_results(self, request, term, page, context):
        idea = request.GET.get('idea', '')
        if idea:
            goals = Idea.objects.get(pk=idea).goal.all()
        else:
            # If idea not present show all goals
            goals = Goal.objects.all()
        s2_results = [(n.id, n.name, {}) for n in goals]
        return ('nil', False, s2_results)


class IdeaChoiceField(AutoModelSelect2Field):
    queryset = Idea.objects

    def get_results(self, request, term, page, context):
        goal = request.GET.get('goal', '')

        if goal:
            ideas = Idea.objects.filter(goal=goal, name__icontains=term)
        else:
            # If goal not pesent show all ideas
            ideas = Idea.objects.all()

        s2_results = [(n.id, n.name, {}) for n in ideas]
        return ('nil', False, s2_results)


class MembersChoiceField(AutoModelSelect2MultipleField):
    queryset = User.objects.all()
    search_fields = ['username__icontains']
