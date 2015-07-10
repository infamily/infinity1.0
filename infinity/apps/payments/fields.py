from django_select2.fields import AutoModelSelect2Field
from django.contrib.auth import get_user_model

User = get_user_model()


class UserChoiceField(AutoModelSelect2Field):
    queryset = User.objects.all()
    search_fields = ['username__icontains', ]
