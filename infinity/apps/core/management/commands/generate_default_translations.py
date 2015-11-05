from django.core.management import BaseCommand
from django.contrib.contenttypes.models import ContentType

from core.models import Translation
from core.models import Goal, Idea, Plan, Step, Task
from core.models import Language

import settings
import pickle
import os

print settings.base.FIXTURE_DIRS


class Command(BaseCommand):
    help = 'generate default translation for each of content types'

    def handle(self, *args, **options):
        content_types = ContentType.objects.get_for_models(Goal, Idea, Plan, Step, Task)

        pickle_file = os.path.join(settings.base.FIXTURE_DIRS[0], 'memorize_languages.pickle')
        memorize_languages = {'goal': {}, 'idea': {}, 'plan': {}, 'step': {}, 'task': {} }

        for model, content_type in content_types.items():
            for instance in model.objects.all():

                translations = Translation.objects.filter(
                    content_type=content_type,
                    object_id=instance.pk
                )

                if translations:
                    continue

                fields = []

                ignored_fields = ['language', 'language_id', 'id']

                for translation_field in Translation._meta.get_all_field_names():
                    for instance_field in instance._meta.get_all_field_names():
                        if instance_field == translation_field:
                            if instance_field in ignored_fields:
                                continue
                            fields.append(translation_field)

                translation = Translation()
                translation.content_type = content_type
                translation.object_id = instance.id

                if not instance.language:

                    if os.path.exists(pickle_file):
                        f = open(pickle_file, 'rb')
                        memorize_languages = pickle.load(f)
                        f.close()

                    if instance.id in memorize_languages[str(content_type)].keys():
                        translation.language = Language.objects.get(
                            id=memorize_languages[str(content_type)][instance.id]
                        )
                    else:
                        try:
                            #print instance
                            language_id = int(raw_input('Language not found. Enter language code: '))
                            translation.language = Language.objects.get(id=language_id)
                            memorize_languages[str(content_type)][instance.id] = translation.language.id
                            pickle.dump(memorize_languages, open(pickle_file, 'wb'))
                        except TypeError:
                            return unicode(instance.id)

                else:
                    translation.language = instance.language

                for field in fields:
                    setattr(translation, field, getattr(instance, field))

                translation.save()
