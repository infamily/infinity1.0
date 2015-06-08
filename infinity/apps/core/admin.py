from django.contrib import admin

from core.models import (
    Comment,
    Transaction,
    Goal,
    Currency,
    Work,
    Idea,
    Platform,
    Step,
    Task,
    User,
    Address,
    Need,
    Type,
    Plan,
)


from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
# admin.site.unregister(SocialApp)
# admin.site.unregister(SocialToken)
# admin.site.unregister(SocialAccount)

admin.site.register(Comment)
admin.site.register(Transaction)
admin.site.register(Goal)
admin.site.register(Currency)
admin.site.register(Work)
admin.site.register(Idea)
admin.site.register(Platform)
admin.site.register(Step)
admin.site.register(Task)
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Need)
admin.site.register(Type)
admin.site.register(Plan)
