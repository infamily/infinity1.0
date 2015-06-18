from django.contrib.contenttypes.models import ContentType
from .forms import CommentCreateFormDetail
from .models import Comment
from django.views.generic import CreateView


class ViewTypeWrapper(object):
    default_view_type = 'list'
    allowed_view_types = [u'list', u'blocks']

    def get_template_names(self):
        """
            Override standart method that return template name

            In view_type transferred the display type
            (value on the basis of which will be decided what kind
            of template to choose: a table, block or gallery).

            This value is stored in the session, and passed to a
            get_template_by_view_type method that returns template
            based on the transmitted view_type
        """

        view_type = self.get_view_type()

        return self.get_template_by_view_type(view_type)

    def get_view_type(self):
        """
        Returns view_type based on the get parameter from session.
        We record a view_type in session,
        if in the get parameter are passed new value

        In get paramater we get view type
        check whether there is a resulting string in the list of allowed view_type
        if the value of view_type correspondence list, then save this value
        back default view_type in session
        """
        view_type = self.request.GET.get('view_type')

        if view_type in self.allowed_view_types:
            self.request.session['view_type'] = view_type
            self.request.session.save()
            return view_type

        view_type = self.request.session.get('view_type')

        return view_type or self.default_view_type

    def get_template_by_view_type(self, view_type):
        """
            Return template name by view type

            :param view_type: on the basis
            of this parameter we define
            how to display the content

            view_type can receive three values: map, gallery, table.
            Depending on the view type.
            For example, if we give view_type value "table",
            then we display page as a table
        """

        if view_type not in self.allowed_view_types:
            view_type = self.default_view_type

        return getattr(self, 'template_name_%s' % view_type, None)

    def get_context_data(self, **kwargs):
        context = super(ViewTypeWrapper, self).get_context_data(**kwargs)
        context['allowed_view_types'] = self.allowed_view_types
        return context


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
