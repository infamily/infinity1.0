from django.contrib import admin

from .models import Comment
from .models import Goal
from .models import Work
from .models import Idea
from .models import Step
from .models import Task
from .models import Need
from .models import Type
from .models import Plan


admin.site.register(Comment)
admin.site.register(Goal)
admin.site.register(Work)
admin.site.register(Idea)
admin.site.register(Step)
admin.site.register(Task)
admin.site.register(Need)
admin.site.register(Type)
admin.site.register(Plan)
