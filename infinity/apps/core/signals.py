def _content_type_post_save(sender, instance, created, *args, **kwargs):
    """
    Create default translation
    """
    from django.contrib.contenttypes.models import ContentType
    from .models import Translation
    content_type = ContentType.objects.get_for_model(sender)

    if created:
        Translation.objects.create(
            content_type=content_type,
            object_id=instance.id,
            language=instance.language,
            default=True
        )
