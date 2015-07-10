from django.conf.urls import patterns, url
from users.views import UserDetailView
from users.views import UserUpdateView
from users.views import UserCryptsyNotificationToken
from users.views import FriendFollowingView
from users.views import FollowView


urlpatterns = patterns(
    '',
    url(
        r'^update/$',
        UserUpdateView.as_view(),
        name="user-update"
    ),
    url(
        r'^(?P<username>.*)/friends/$',
        FriendFollowingView.as_view(),
        name="friend-following"
    ),
    url(
        r'^follow/$',
        FollowView.as_view(),
        name='follow'
    ),
    url(
        r'^(?P<slug>.*)/$',
        UserDetailView.as_view(),
        name="user-detail"
    ),
    url(
        r'^(?P<username>.*)/cryptsy/(?P<credential_id>\d+)/checkpoint/$',
        UserCryptsyNotificationToken.as_view(),
        name='cryptsy_notification_token'
    )
)
