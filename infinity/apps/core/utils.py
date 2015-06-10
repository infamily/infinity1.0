from django.contrib.contenttypes.models import ContentType
from .forms import CommentCreateFormDetail
from .models import Comment
from django.views.generic import CreateView
from payments.models import CryptsyTransaction
from payments.models import PayPalTransaction


class CommentsContentTypeWrapper(CreateView):
    model_for_list = Comment

    form_class = CommentCreateFormDetail

    @property
    def object_list(self):
        goal_content_type = ContentType.objects.get_for_model(
            self.get_object()
        )
        object_list = self.model_for_list.objects.filter(
            content_type__pk=goal_content_type.pk,
            object_id=self.get_object().id
        )

        return object_list.order_by('-id')

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.content_type = ContentType.objects.get_for_model(self.get_object())
        self.object.object_id = self.get_object().id
        self.object.save()
        return super(CommentsContentTypeWrapper, self).form_valid(form)
