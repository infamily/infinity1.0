from django.core.management import BaseCommand
from django.contrib.contenttypes.models import ContentType

from core.models import Translation
from core.models import Goal, Idea, Plan, Step, Task


class Command(BaseCommand):
    help = 'generate default translation for each of content types'

    def handle(self, *args, **options):
        content_types = ContentType.objects.get_for_models(Goal, Idea, Plan, Step, Task)

        for model, content_type in content_types.items():
            for instance in model.objects.all():
                default_translations = Translation.objects.filter(
                    default=True,
                    content_type=content_type,
                    object_id=instance.pk
                )

                if not default_translations:
                    Translation.objects.create(
                        default=True,
                        content_type=content_type,
                        object_id=instance.pk
                    )
