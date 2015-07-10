def user_pre_save(sender, instance, *args, **kwargs):
    """ Get username from email
    sender - The model class.
    instance - The actual instance being saved.
    created - Boolean; True if a new record was created.

    *args, **kwargs - Capture the unneeded `raw` and `using` arguments.
    """
    import random
    import string

    def randomword(length):
        """
        Random string generator
        """
        return ''.join(random.choice(string.lowercase) for i in range(length))

    if not instance.username:
        username = '%s-%s' % (randomword(10), instance.email.split('@')[0])
        instance.username = username
        instance.save()
