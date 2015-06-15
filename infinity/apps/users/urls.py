from django.conf.urls import patterns, url
from users.views import login, register, UserDetailView, UserUpdateView


urlpatterns = patterns(
    '',
    url("^login/$", login, name="login"),
    url("^register/$", register, name="register"),
    url(
        r'^me/$',
        UserDetailView.as_view(),
        name="user-detail"
    ),
    url(
        r'^me/update/$',
        UserUpdateView.as_view(),
        name="user-update"
    ),
)
