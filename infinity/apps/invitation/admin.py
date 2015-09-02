from django.contrib import admin

from .models import Invitation
from .models import InvitationLetterTemplate
from .models import InvitationOption


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'email', 'has_accepted_invitation', )

admin.site.register(Invitation, InvitationAdmin)
admin.site.register(InvitationLetterTemplate)
admin.site.register(InvitationOption)
