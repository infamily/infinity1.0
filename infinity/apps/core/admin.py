from django.contrib import admin

from core.models import (
    Comment,
    Goal,
    Work,
    Idea,
    Step,
    Task,
    User,
    Need,
    Type,
    Plan,
)


from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)

admin.site.register(Comment)
admin.site.register(Goal)
admin.site.register(Work)
admin.site.register(Idea)
admin.site.register(Step)
admin.site.register(Task)
admin.site.register(User)
admin.site.register(Need)
admin.site.register(Type)
admin.site.register(Plan)
