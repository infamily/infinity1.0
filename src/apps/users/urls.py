from django.conf.urls import url
from users.views import *

from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = [
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
        r'^i/(?P<object_name>.*)/(?P<object_id>\d+)/$',
        staff_member_required(
            ConversationInviteView.as_view(),
        ),
        name="user-conversation-invite"
    ),
    url(
        r'^i/(?P<token>.*)/$',
        staff_member_required(
            ConversationInviteView.as_view(),
        ),
        name="user-conversation-invite"
    ),
    url(
        r'^(?P<slug>.*)/$',
        UserDetailView.as_view(),
        name="user-detail"
    ),
]
