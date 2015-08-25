from django_select2.fields import AutoModelSelect2Field

from .models import Need
from .models import Type


class NeedChoiceField(AutoModelSelect2Field):
    queryset = Need.objects

    def get_results(self, request, term, page, context):
        _type = request.GET.get('type', '')
        needs = Need.objects.filter(type=_type, name__istartswith=term)
        s2_results = [(n.id, n.name, {}) for n in needs]
        if not s2_results:
            return ('nil', False, [(None, term, {})])
        return ('nil', False, s2_results)


class TypeChoiceField(AutoModelSelect2Field):
    queryset = Type.objects

    def get_results(self, request, term, page, context):
        types = Type.objects.all()
        s2_results = [(n.id, n.name, {}) for n in types]
        return ('nil', False, s2_results)
