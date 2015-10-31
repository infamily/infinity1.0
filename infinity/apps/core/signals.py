def _content_type_post_save(sender, instance, created, *args, **kwargs):
    """
    Create default translation
    """
    from django.contrib.contenttypes.models import ContentType
    from .models import Translation
    content_type = ContentType.objects.get_for_model(sender)

    # Get Field List from Translation model
    fields = []
    ignored_fields = ['language', 'language_id', 'id']
    for translation_field in Translation._meta.get_all_field_names():
        for instance_field in instance._meta.get_all_field_names():
            if instance_field == translation_field:
                if instance_field in ignored_fields:
                    continue
                fields.append(translation_field)

    if created:
        translation = Translation()
        translation.content_type = content_type
        translation.object_id = instance.id
        translation.language = instance.language

        for field in fields:
            setattr(translation, field, getattr(instance, field))

        translation.save()
    else:
        translation = Translation.objects.get(
            content_type=content_type, object_id=instance.id
        )

        for field in fields:
            setattr(translation, field, getattr(instance, field))
        translation.save()
