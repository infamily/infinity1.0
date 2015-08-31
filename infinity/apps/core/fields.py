from django_select2.fields import AutoModelSelect2Field

from .models import Need
from .models import Type
from .models import Goal
from .models import Idea


class TypeChoiceField(AutoModelSelect2Field):
    queryset = Type.objects

    def get_results(self, request, term, page, context):
        types = Type.objects.all()
        s2_results = [(n.id, n.name, {}) for n in types]
        return ('nil', False, s2_results)


class NeedChoiceField(AutoModelSelect2Field):
    queryset = Need.objects

    def get_results(self, request, term, page, context):
        # _type = request.GET.get('type', '')
        needs = Need.objects.filter(name__istartswith=term)
        s2_results = [(n.id, "(%s) %s: %s" %
                       (n.language.name,n.name,n.definition), {}) for n in needs]
        return ('nil', False, s2_results)


class GoalChoiceField(AutoModelSelect2Field):
    queryset = Goal.objects

    def get_results(self, request, term, page, context):
        # need = request.GET.get('need', '')
        goals = Goal.objects.filter(name__icontains=term)
        s2_results = [(n.id, n.name, {}) for n in goals]
        return ('nil', False, s2_results)


class IdeaChoiceField(AutoModelSelect2Field):
    queryset = Idea.objects

    def get_results(self, request, term, page, context):
        goal = request.GET.get('goal', '')
        ideas = Idea.objects.filter(goal=goal,name__icontains=term)
        s2_results = [(n.id, n.name, {}) for n in ideas]
        return ('nil', False, s2_results)

