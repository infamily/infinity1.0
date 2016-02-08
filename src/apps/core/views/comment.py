from django.views.generic import View
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.contrib import messages
from django.utils.translation import ugettext as _
import re

from ..forms import CommentUpdateForm
from ..models import Comment, Vote
from users.mixins import OwnerMixin

from ..utils import JsonView
from ..utils import update_child_paypal_transactions

class AjaxCommentVoteView(JsonView):
    """
    Vote view
    """
    def post(self, request, *args, **kwargs):

        votes = Vote.objects.filter(
            comment_id=request.POST['comment_id'],
            user_id=request.user.id)

        if votes.exists():
			vote = votes[0]
        else:
            vote = Vote.objects.create(
                comment_id=request.POST['comment_id'],
                value=request.POST['vote_value'],
                user_id=request.user.id)
            vote.save()

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

        return self.json(response)


class CommentUpdateView(OwnerMixin, UpdateView):

    """Comment update view"""
    model = Comment
    form_class = CommentUpdateForm
    slug_field = "pk"
    template_name = "comment/update.html"

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        messages.success(self.request, _("Comment succesfully updated"))

        # We want to update here the comment's transactions to compute .hours_matched
        comment_regxp = re.compile('comment/(\d+)/update')
        is_match = comment_regxp.search(self.request.path)
        if is_match:
            comment_id = int(is_match.group(1))
            comment = Comment.objects.get(pk=comment_id)
            update_child_paypal_transactions(comment)

        if next_url:
            return next_url
        return "/"


class CommentDeleteView(DeleteView):

    """Comment delete view"""
    model = Comment
    slug_field = "pk"
    template_name = "comment/delete.html"

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        messages.success(self.request, _("Comment succesfully deleted"))
        if next_url:
            return next_url
        return "/"
