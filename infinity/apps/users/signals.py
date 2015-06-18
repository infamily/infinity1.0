def user_post_save(sender, instance, created, *args, **kwargs):
    """
    Get username from email
    """
    if created:
        username = instance.email.split('@')[0]
        instance.username = username
        instance.save()
