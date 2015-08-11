def _comment_post_save(sender, instance, created, *args, **kwargs):
    """
    After the user save comment, send e-mail notifications
    """
    from users.models import User
    from constance import config
    from os import path
    from re import finditer

    subject_template_path='mail/comments/mention_notification_subject.txt'
    email_template_path='mail/comments/mention_notification.html'

    if instance.notify:

        comment = instance.text
        usernames = [m.group(1) for m in finditer('\[([^]]+)\]', comment)]
        usernames = usernames[:config.MAX_MENTIONS_PER_COMMENT]

        users = User.objects.filter(username__in=usernames)

        if users.exists():

            from .utils import send_mail_template
            from django.contrib.sites.models import Site

            url = "%s/%s/detail/#" % (instance.content_type,
                                      instance.content_object.id)
            link = path.join(path.join('http://', Site.objects.get_current().domain), url)
            

            for user in users.iterator():

                send_mail_template(subject_template_path,
                                    email_template_path,
                                    recipient_list=[user.email],
                                    context={'user': instance.user.username,
                                             'comment': instance.text,
                                             'link': link})
