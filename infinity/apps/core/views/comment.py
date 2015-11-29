from django.views.generic import View
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.contrib import messages
from django.utils.translation import ugettext as _

from braces.views import AjaxResponseMixin
from braces.views import JSONResponseMixin

from ..forms import CommentUpdateForm
from ..models import Comment, Vote
from users.mixins import OwnerMixin


class AjaxCommentVoteView(JSONResponseMixin, AjaxResponseMixin, View):
    """
    Vote view
    """
    def post_ajax(self, request, *args, **kwargs):

        try:
            vote = Vote.objects.get(
                comment_id=request.POST['comment_id'],
                user_id=request.user.id)
        except:
            vote = Vote.objects.create(
                comment_id=request.POST['comment_id'],
                value=request.POST['vote_value'],
                user_id=request.user.id)
            vote.save()

        if 'vote' in locals():
            if vote.value == int(request.POST['vote_value']):
                if vote.value != 0:
                    vote.value = 0
                    vote.save()
                else:
                    vote.value = int(request.POST['vote_value'])
                    vote.save()
            else:
                vote.value = int(request.POST['vote_value'])
                vote.save()

            response = {'value': vote.value,
                        'total': vote.comment.votes(),
                        'success': True,
                        'comment_id': vote.comment.id,
                        'total_comment_credit': vote.comment.comment_credit()}

        else:
            response = {'success': False}

        return self.render_json_response(response)


class CommentUpdateView(OwnerMixin, UpdateView):

    """Comment update view"""
    model = Comment
    form_class = CommentUpdateForm
    slug_field = "pk"
    template_name = "comment/update.html"

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        messages.success(self.request, _("Comment succesfully updated"))
        if next_url:
            return next_url
        return "/"


class CommentDeleteView(DeleteView):

    """Comment delete view"""
    model = Comment
    slug_field = "pk"
    template_name = "comment/delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Comment succesfully deleted"))
        return "/"
