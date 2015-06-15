from django.contrib import admin

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialToken

from .models import User

admin.site.register(User)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
