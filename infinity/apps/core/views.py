from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView, ListView
)

from pure_pagination.mixins import PaginationMixin
from braces.views import OrderableListMixin
from enhanced_cbv.views import ListFilteredView
from allauth.account.utils import complete_signup
from allauth.account.app_settings import EMAIL_VERIFICATION

from .decorators import ForbiddenUser

from .forms import LoginForm
from .forms import SignUpUserForm

from core.models import (
    Comment,
    Transaction,
    Goal,
    Currency,
    Work,
    Idea,
    Platform,
    Step,
    Task,
    User,
    Address,
    Need,
    Type,
    Plan,
)
from core.forms import (
    CommentUpdateForm,
    CommentCreateForm,
    GoalCreateForm1,
    GoalUpdateForm,
    GoalCreateForm2,
    WorkUpdateForm,
    WorkCreateForm,
    IdeaUpdateForm,
    IdeaCreateForm,
    StepUpdateForm,
    StepCreateForm,
    TaskUpdateForm,
    TaskCreateForm,
    UserUpdateForm,
    NeedCreateForm,
    PlanUpdateForm,
    PlanCreateForm,
)

from core.forms import CommentCreateFormDetail
from core.forms import CommentCreateFormDetail
from core.forms import CommentCreateFormDetail
from core.forms import CommentCreateFormDetail
from core.forms import CommentCreateFormDetail
from core.forms import CommentCreateFormDetail
from core.forms import CommentCreateFormDetail


from core.filters import (
    CommentListViewFilter1,
    CommentListViewFilter2,
    GoalListViewFilter1,
    GoalListViewFilter2,
    WorkListViewFilter1,
    WorkListViewFilter2,
    IdeaListViewFilter1,
    IdeaListViewFilter2,
    StepListViewFilter1,
    StepListViewFilter2,
    TaskListViewFilter1,
    TaskListViewFilter2,
    NeedListViewFilter,
    PlanListViewFilter1,
    PlanListViewFilter2,
)


class CommentListView1(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Comment list view"""
    default_view_type = 'list'
    allowed_view_types = [u'list', u'blocks']
    template_name_list = "comment-list1.html"
    template_name_blocks = "comment-blocks1.html"

    model = Comment
    paginate_by = 10
    orderable_columns = [
        "task",
        "goal",
        "text",
        "created_at",
        "work",
        "updated_at",
        "idea",
        "step",
        "user",
        "plan",
    ]
    orderable_columns_default = "-id"
    filter_set = CommentListViewFilter1

    def get_base_queryset(self):
        queryset = super(CommentListView1, self).get_base_queryset()
        queryset = queryset.filter(user=self.request.user.pk)
        return queryset

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
        context = super(CommentListView1, self).get_context_data(
            **kwargs)
        context['allowed_view_types'] = self.allowed_view_types
        return context


class CommentUpdateView(UpdateView):

    """Comment update view"""
    model = Comment
    form_class = CommentUpdateForm
    slug_field = "pk"
    template_name = "comment-update.html"

    def get_success_url(self):
        messages.success(self.request, _("Comment succesfully updated"))
        return "/"


class CommentDeleteView(DeleteView):

    """Comment delete view"""
    model = Comment
    slug_field = "pk"
    template_name = "comment-delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Comment succesfully deleted"))
        return "/"


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class CommentListView2(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Comment list view"""

    template_name = "comment-list2.html"

    model = Comment
    paginate_by = 10
    orderable_columns = [
        "task",
        "goal",
        "text",
        "created_at",
        "work",
        "updated_at",
        "idea",
        "step",
        "user",
        "plan",
    ]
    orderable_columns_default = "-id"
    filter_set = CommentListViewFilter2

    def get_base_queryset(self):
        queryset = super(CommentListView2, self).get_base_queryset()
        queryset = queryset.filter(goal__pk=self.kwargs['goal'])
        return queryset


class CommentCreateView(CreateView):

    """Comment create view"""
    model = Comment
    form_class = CommentCreateForm
    template_name = "comment-create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CommentCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Comment succesfully created"))
        return "/"


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class GoalCreateView1(CreateView):

    """Goal create view"""
    model = Goal
    form_class = GoalCreateForm1
    template_name = "goal-create1.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.need = Need.objects.get(pk=self.kwargs['need'])
        self.object.save()
        return super(GoalCreateView1, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Goal succesfully created"))
        return reverse("goal-detail", args=[self.object.pk, ])


class GoalListView1(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Goal list view"""
    default_view_type = 'list'
    allowed_view_types = [u'list', u'blocks']
    template_name_list = "goal-list1.html"
    template_name_blocks = "goal-blocks1.html"

    model = Goal
    paginate_by = 10
    orderable_columns = [
        "name",
        "personal",
        "created_at",
        "updated_at",
        "reason",
        "user",
        "need",
        "quantity",
    ]
    orderable_columns_default = "-id"
    filter_set = GoalListViewFilter1

    def get_base_queryset(self):
        queryset = super(GoalListView1, self).get_base_queryset()
        queryset = queryset.filter(need__pk=self.kwargs['need'])
        return queryset

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
        context = super(GoalListView1, self).get_context_data(
            **kwargs)
        context['allowed_view_types'] = self.allowed_view_types
        return context


class GoalDeleteView(DeleteView):

    """Goal delete view"""
    model = Goal
    slug_field = "pk"
    template_name = "goal-delete.html"

    def get_object(self, queryset=None):
        obj = super(GoalDeleteView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can delete Goal")
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Goal succesfully deleted"))
        return reverse("goal-list1", args=[self.object.need.pk, ])


class GoalUpdateView(UpdateView):

    """Goal update view"""
    model = Goal
    form_class = GoalUpdateForm
    slug_field = "pk"
    template_name = "goal-update.html"

    def get_object(self, queryset=None):
        obj = super(GoalUpdateView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can update Goal")
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(GoalUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Goal succesfully updated"))
        return reverse("goal-list1", args=[self.object.need.pk, ])


class GoalDetailView(DetailView, CreateView):

    """Goal detail view"""
    model = Goal
    slug_field = "pk"
    template_name = "goal-detail.html"

    model_for_list = Comment

    form_class = CommentCreateFormDetail

    @property
    def object_list(self):
        object_list = self.model_for_list.objects.filter(
            goal=self.get_object(),
        )
        return object_list.order_by('-id')

    def get_success_url(self):
        messages.success(
            self.request, _(
                "%s succesfully created" %
                self.form_class._meta.model.__name__))
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(GoalDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        form = None
        if self.request.user.__class__.__name__ not in [u'AnonymousUser']:
            form = self.get_form_class()
        context.update({
            'form': form,
        })
        context.update({
            'object_list': self.object_list,
        })
        return context

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.goal = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super(GoalDetailView, self).form_valid(form)


class GoalListView2(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Goal list view"""
    default_view_type = 'list'
    allowed_view_types = [u'list', u'blocks']
    template_name_list = "goal-list2.html"
    template_name_blocks = "goal-blocks2.html"

    model = Goal
    paginate_by = 10
    orderable_columns = [
        "name",
        "personal",
        "created_at",
        "updated_at",
        "reason",
        "user",
        "need",
        "quantity",
    ]
    orderable_columns_default = "-id"
    filter_set = GoalListViewFilter2

    def get_base_queryset(self):
        queryset = super(GoalListView2, self).get_base_queryset()
        queryset = queryset.filter(need__pk=self.kwargs['need'])
        return queryset

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
        context = super(GoalListView2, self).get_context_data(
            **kwargs)
        context['allowed_view_types'] = self.allowed_view_types
        return context


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class GoalCreateView2(CreateView):

    """Goal create view"""
    model = Goal
    form_class = GoalCreateForm2
    template_name = "goal-create2.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.need = Need.objects.get(pk=self.kwargs['need'])
        self.object.save()
        return super(GoalCreateView2, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Goal succesfully created"))
        return "/"


class WorkListView1(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Work list view"""
    default_view_type = 'list'
    allowed_view_types = [u'list', u'blocks']
    template_name_list = "work-list1.html"
    template_name_blocks = "work-blocks1.html"

    model = Work
    paginate_by = 10
    orderable_columns = [
        "task",
        "name",
        "url",
        "created_at",
        "updated_at",
        "user",
        "file",
        "parent_work_id",
        "description",
    ]
    orderable_columns_default = "-id"
    filter_set = WorkListViewFilter1

    def get_base_queryset(self):
        queryset = super(WorkListView1, self).get_base_queryset()
        queryset = queryset.filter(task__pk=self.kwargs['task'])
        return queryset

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
        context = super(WorkListView1, self).get_context_data(
            **kwargs)
        context['allowed_view_types'] = self.allowed_view_types
        return context


class WorkUpdateView(UpdateView):

    """Work update view"""
    model = Work
    form_class = WorkUpdateForm
    slug_field = "pk"
    template_name = "work-update.html"

    def get_object(self, queryset=None):
        obj = super(WorkUpdateView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can update Work")
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(WorkUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Work succesfully updated"))
        return reverse("work-list1", args=[self.object.task.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class WorkCreateView(CreateView):

    """Work create view"""
    model = Work
    form_class = WorkCreateForm
    template_name = "work-create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.task = Task.objects.get(pk=self.kwargs['task'])
        self.object.save()
        return super(WorkCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Work succesfully created"))
        return reverse("work-detail", args=[self.object.pk, ])


class WorkDeleteView(DeleteView):

    """Work delete view"""
    model = Work
    slug_field = "pk"
    template_name = "work-delete.html"

    def get_object(self, queryset=None):
        obj = super(WorkDeleteView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can delete Work")
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Work succesfully deleted"))
        return reverse("work-list1", args=[self.object.task.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class WorkListView2(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Work list view"""
    default_view_type = 'list'
    allowed_view_types = [u'list', u'blocks']
    template_name_list = "work-list2.html"
    template_name_blocks = "work-blocks2.html"

    model = Work
    paginate_by = 10
    orderable_columns = [
        "task",
        "name",
        "url",
        "created_at",
        "updated_at",
        "user",
        "file",
        "parent_work_id",
        "description",
    ]
    orderable_columns_default = "-id"
    filter_set = WorkListViewFilter2

    def get_base_queryset(self):
        queryset = super(WorkListView2, self).get_base_queryset()
        queryset = queryset.filter(user=self.request.user.pk)
        return queryset

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
        context = super(WorkListView2, self).get_context_data(
            **kwargs)
        context['allowed_view_types'] = self.allowed_view_types
        return context


class WorkDetailView(DetailView, CreateView):

    """Work detail view"""
    model = Work
    slug_field = "pk"
    template_name = "work-detail.html"

    model_for_list = Comment

    form_class = CommentCreateFormDetail

    @property
    def object_list(self):
        object_list = self.model_for_list.objects.filter(
            work=self.get_object(),
        )
        return object_list.order_by('-id')

    def get_success_url(self):
        messages.success(
            self.request, _(
                "%s succesfully created" %
                self.form_class._meta.model.__name__))
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(WorkDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        form = None
        if self.request.user.__class__.__name__ not in [u'AnonymousUser']:
            form = self.get_form_class()
        context.update({
            'form': form,
        })
        context.update({
            'object_list': self.object_list,
        })
        return context

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.work = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super(WorkDetailView, self).form_valid(form)


class IdeaListView1(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Idea list view"""
    default_view_type = 'list'
    allowed_view_types = [u'list', u'blocks']
    template_name_list = "idea-list1.html"
    template_name_blocks = "idea-blocks1.html"

    model = Idea
    paginate_by = 10
    orderable_columns = [
        "description",
        "name",
        "created_at",
        "updated_at",
        "summary",
        "user",
        "goal",
    ]
    orderable_columns_default = "-id"
    filter_set = IdeaListViewFilter1

    def get_base_queryset(self):
        queryset = super(IdeaListView1, self).get_base_queryset()
        queryset = queryset.filter(goal__pk=self.kwargs['goal'])
        return queryset

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
        context = super(IdeaListView1, self).get_context_data(
            **kwargs)
        context['allowed_view_types'] = self.allowed_view_types
        return context


class IdeaUpdateView(UpdateView):

    """Idea update view"""
    model = Idea
    form_class = IdeaUpdateForm
    slug_field = "pk"
    template_name = "idea-update.html"

    def get_object(self, queryset=None):
        obj = super(IdeaUpdateView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can update Idea")
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(IdeaUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Idea succesfully updated"))
        return reverse("idea-list1", args=[self.object.goal.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class IdeaCreateView(CreateView):

    """Idea create view"""
    model = Idea
    form_class = IdeaCreateForm
    template_name = "idea-create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.goal = Goal.objects.get(pk=self.kwargs['goal'])
        self.object.save()
        return super(IdeaCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Idea succesfully created"))
        return reverse("idea-detail", args=[self.object.pk, ])


class IdeaDeleteView(DeleteView):

    """Idea delete view"""
    model = Idea
    slug_field = "pk"
    template_name = "idea-delete.html"

    def get_object(self, queryset=None):
        obj = super(IdeaDeleteView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can delete Idea")
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Idea succesfully deleted"))
        return reverse("idea-list1", args=[self.object.goal.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class IdeaListView2(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Idea list view"""
    default_view_type = 'list'
    allowed_view_types = [u'list', u'blocks']
    template_name_list = "idea-list2.html"
    template_name_blocks = "idea-blocks2.html"

    model = Idea
    paginate_by = 10
    orderable_columns = [
        "description",
        "name",
        "created_at",
        "updated_at",
        "summary",
        "user",
        "goal",
    ]
    orderable_columns_default = "-id"
    filter_set = IdeaListViewFilter2

    def get_base_queryset(self):
        queryset = super(IdeaListView2, self).get_base_queryset()
        queryset = queryset.filter(user=self.request.user.pk)
        return queryset

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
        context = super(IdeaListView2, self).get_context_data(
            **kwargs)
        context['allowed_view_types'] = self.allowed_view_types
        return context


class IdeaDetailView(DetailView, CreateView):

    """Idea detail view"""
    model = Idea
    slug_field = "pk"
    template_name = "idea-detail.html"

    model_for_list = Comment

    form_class = CommentCreateFormDetail

    @property
    def object_list(self):
        object_list = self.model_for_list.objects.filter(
            idea=self.get_object(),
        )
        return object_list.order_by('-id')

    def get_success_url(self):
        messages.success(
            self.request, _(
                "%s succesfully created" %
                self.form_class._meta.model.__name__))
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(IdeaDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        form = None
        if self.request.user.__class__.__name__ not in [u'AnonymousUser']:
            form = self.get_form_class()
        context.update({
            'form': form,
        })
        context.update({
            'object_list': self.object_list,
        })
        return context

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.idea = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super(IdeaDetailView, self).form_valid(form)


class StepListView1(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Step list view"""
    default_view_type = 'list'
    allowed_view_types = [u'list', u'blocks']
    template_name_list = "step-list1.html"
    template_name_blocks = "step-blocks1.html"

    model = Step
    paginate_by = 10
    orderable_columns = [
        "user",
        "name",
        "created_at",
        "updated_at",
        "deliverables",
        "priority",
        "plan",
        "objective",
        "investables",
    ]
    orderable_columns_default = "-id"
    filter_set = StepListViewFilter1

    def get_base_queryset(self):
        queryset = super(StepListView1, self).get_base_queryset()
        queryset = queryset.filter(plan__pk=self.kwargs['plan'])
        return queryset

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
        context = super(StepListView1, self).get_context_data(
            **kwargs)
        context['allowed_view_types'] = self.allowed_view_types
        return context


class StepUpdateView(UpdateView):

    """Step update view"""
    model = Step
    form_class = StepUpdateForm
    slug_field = "pk"
    template_name = "step-update.html"

    def get_object(self, queryset=None):
        obj = super(StepUpdateView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can update Step")
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(StepUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Step succesfully updated"))
        return reverse("step-list1", args=[self.object.plan.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class StepCreateView(CreateView):

    """Step create view"""
    model = Step
    form_class = StepCreateForm
    template_name = "step-create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.plan = Plan.objects.get(pk=self.kwargs['plan'])
        self.object.save()
        return super(StepCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Step succesfully created"))
        return reverse("step-detail", args=[self.object.pk, ])


class StepDeleteView(DeleteView):

    """Step delete view"""
    model = Step
    slug_field = "pk"
    template_name = "step-delete.html"

    def get_object(self, queryset=None):
        obj = super(StepDeleteView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can delete Step")
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Step succesfully deleted"))
        return reverse("step-list1", args=[self.object.plan.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class StepListView2(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Step list view"""
    default_view_type = 'list'
    allowed_view_types = [u'list', u'blocks']
    template_name_list = "step-list2.html"
    template_name_blocks = "step-blocks2.html"

    model = Step
    paginate_by = 10
    orderable_columns = [
        "user",
        "name",
        "created_at",
        "updated_at",
        "deliverables",
        "priority",
        "plan",
        "objective",
        "investables",
    ]
    orderable_columns_default = "-id"
    filter_set = StepListViewFilter2

    def get_base_queryset(self):
        queryset = super(StepListView2, self).get_base_queryset()
        queryset = queryset.filter(user=self.request.user.pk)
        return queryset

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
        context = super(StepListView2, self).get_context_data(
            **kwargs)
        context['allowed_view_types'] = self.allowed_view_types
        return context


class StepDetailView(DetailView, CreateView):

    """Step detail view"""
    model = Step
    slug_field = "pk"
    template_name = "step-detail.html"

    model_for_list = Comment

    form_class = CommentCreateFormDetail

    @property
    def object_list(self):
        object_list = self.model_for_list.objects.filter(
            step=self.get_object(),
        )
        return object_list.order_by('-id')

    def get_success_url(self):
        messages.success(
            self.request, _(
                "%s succesfully created" %
                self.form_class._meta.model.__name__))
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(StepDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        form = None
        if self.request.user.__class__.__name__ not in [u'AnonymousUser']:
            form = self.get_form_class()
        context.update({
            'form': form,
        })
        context.update({
            'object_list': self.object_list,
        })
        return context

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.step = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super(StepDetailView, self).form_valid(form)


class TaskListView1(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Task list view"""
    default_view_type = 'list'
    allowed_view_types = [u'list', u'blocks']
    template_name_list = "task-list1.html"
    template_name_blocks = "task-blocks1.html"

    model = Task
    paginate_by = 10
    orderable_columns = [
        "name",
        "created_at",
        "updated_at",
        "priority",
        "step",
        "user",
    ]
    orderable_columns_default = "-id"
    filter_set = TaskListViewFilter1

    def get_base_queryset(self):
        queryset = super(TaskListView1, self).get_base_queryset()
        queryset = queryset.filter(step__pk=self.kwargs['step'])
        return queryset

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
        context = super(TaskListView1, self).get_context_data(
            **kwargs)
        context['allowed_view_types'] = self.allowed_view_types
        return context


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class TaskUpdateView(UpdateView):

    """Task update view"""
    model = Task
    form_class = TaskUpdateForm
    slug_field = "pk"
    template_name = "task-update.html"

    def get_object(self, queryset=None):
        obj = super(TaskUpdateView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can update Task")
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(TaskUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Task succesfully updated"))
        return reverse("task-list1", args=[self.object.step.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class TaskCreateView(CreateView):

    """Task create view"""
    model = Task
    form_class = TaskCreateForm
    template_name = "task-create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.step = Step.objects.get(pk=self.kwargs['step'])
        self.object.save()
        return super(TaskCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Task succesfully created"))
        return reverse("task-detail", args=[self.object.pk, ])


class TaskDeleteView(DeleteView):

    """Task delete view"""
    model = Task
    slug_field = "pk"
    template_name = "task-delete.html"

    def get_object(self, queryset=None):
        obj = super(TaskDeleteView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can delete Task")
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Task succesfully deleted"))
        return reverse("task-list1", args=[self.object.step.pk, ])


class TaskListView2(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Task list view"""

    template_name = "task-list2.html"

    model = Task
    paginate_by = 10
    orderable_columns = [
        "name",
        "created_at",
        "updated_at",
        "priority",
        "step",
        "user",
    ]
    orderable_columns_default = "-id"
    filter_set = TaskListViewFilter2

    def get_base_queryset(self):
        queryset = super(TaskListView2, self).get_base_queryset()
        queryset = queryset.filter(user=self.request.user.pk)
        return queryset


class TaskDetailView(DetailView, CreateView):

    """Task detail view"""
    model = Task
    slug_field = "pk"
    template_name = "task-detail.html"

    model_for_list = Comment

    form_class = CommentCreateFormDetail

    @property
    def object_list(self):
        object_list = self.model_for_list.objects.filter(
            task=self.get_object(),
        )
        return object_list.order_by('-id')

    def get_success_url(self):
        messages.success(
            self.request, _(
                "%s succesfully created" %
                self.form_class._meta.model.__name__))
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        form = None
        if self.request.user.__class__.__name__ not in [u'AnonymousUser']:
            form = self.get_form_class()
        context.update({
            'form': form,
        })
        context.update({
            'object_list': self.object_list,
        })
        return context

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.task = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super(TaskDetailView, self).form_valid(form)


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class UserDetailView(DetailView):

    """User detail view"""
    model = User
    slug_field = "pk"
    template_name = "user-detail.html"

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class UserUpdateView(UpdateView):

    """User update view"""
    model = User
    form_class = UserUpdateForm
    slug_field = "pk"
    template_name = "user-update.html"

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def get_success_url(self):
        messages.success(self.request, _("User succesfully updated"))
        return reverse("user-detail", args=[])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class NeedCreateView(CreateView):

    """Need create view"""
    model = Need
    form_class = NeedCreateForm
    template_name = "need-create.html"

    def get_success_url(self):
        messages.success(self.request, _("Need succesfully created"))
        return reverse("goal-create1", args=[self.object.pk, ])


class NeedListView(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Need list view"""
    default_view_type = 'list'
    allowed_view_types = [u'list', u'blocks']
    template_name_list = "need-list.html"
    template_name_blocks = "need-blocks.html"

    model = Need
    paginate_by = 10
    orderable_columns = ["created_at", "type", "name", ]
    orderable_columns_default = "-id"
    filter_set = NeedListViewFilter

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
        context = super(NeedListView, self).get_context_data(
            **kwargs)
        context['allowed_view_types'] = self.allowed_view_types
        return context


class NeedDetailView(DetailView, CreateView):

    """Need detail view"""
    model = Need
    slug_field = "pk"
    template_name = "need-detail.html"

    model_for_list = Comment

    form_class = CommentCreateFormDetail

    @property
    def object_list(self):
        object_list = self.model_for_list.objects.all()
        return object_list.order_by('-id')

    def get_success_url(self):
        messages.success(
            self.request, _(
                "%s succesfully created" %
                self.form_class._meta.model.__name__))
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(NeedDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        form = None
        if self.request.user.__class__.__name__ not in [u'AnonymousUser']:
            form = self.get_form_class()
        context.update({
            'form': form,
        })
        context.update({
            'object_list': self.object_list,
        })
        return context

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(NeedDetailView, self).form_valid(form)


class PlanListView1(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Plan list view"""
    default_view_type = 'list'
    allowed_view_types = [u'list', u'blocks']
    template_name_list = "plan-list1.html"
    template_name_blocks = "plan-blocks1.html"

    model = Plan
    paginate_by = 10
    orderable_columns = [
        "name",
        "created_at",
        "updated_at",
        "idea",
        "deliverable",
        "user",
        "situation",
    ]
    orderable_columns_default = "-id"
    filter_set = PlanListViewFilter1

    def get_base_queryset(self):
        queryset = super(PlanListView1, self).get_base_queryset()
        queryset = queryset.filter(idea__pk=self.kwargs['idea'])
        return queryset

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
        context = super(PlanListView1, self).get_context_data(
            **kwargs)
        context['allowed_view_types'] = self.allowed_view_types
        return context


class PlanUpdateView(UpdateView):

    """Plan update view"""
    model = Plan
    form_class = PlanUpdateForm
    slug_field = "pk"
    template_name = "plan-update.html"

    def get_object(self, queryset=None):
        obj = super(PlanUpdateView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can update Plan")
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(PlanUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Plan succesfully updated"))
        return reverse("plan-list1", args=[self.object.idea.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class PlanCreateView(CreateView):

    """Plan create view"""
    model = Plan
    form_class = PlanCreateForm
    template_name = "plan-create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.idea = Idea.objects.get(pk=self.kwargs['idea'])
        self.object.save()
        return super(PlanCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Plan succesfully created"))
        return reverse("plan-detail", args=[self.object.pk, ])


class PlanDeleteView(DeleteView):

    """Plan delete view"""
    model = Plan
    slug_field = "pk"
    template_name = "plan-delete.html"

    def get_object(self, queryset=None):
        obj = super(PlanDeleteView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can delete Plan")
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Plan succesfully deleted"))
        return reverse("plan-list1", args=[self.object.idea.pk, ])


class PlanListView2(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Plan list view"""
    default_view_type = 'list'
    allowed_view_types = [u'list', u'blocks']
    template_name_list = "plan-list2.html"
    template_name_blocks = "plan-blocks2.html"

    model = Plan
    paginate_by = 10
    orderable_columns = [
        "name",
        "created_at",
        "updated_at",
        "idea",
        "deliverable",
        "user",
        "situation",
    ]
    orderable_columns_default = "-id"
    filter_set = PlanListViewFilter2

    def get_base_queryset(self):
        queryset = super(PlanListView2, self).get_base_queryset()
        queryset = queryset.filter(user=self.request.user.pk)
        return queryset

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
        context = super(PlanListView2, self).get_context_data(
            **kwargs)
        context['allowed_view_types'] = self.allowed_view_types
        return context


class PlanDetailView(DetailView, CreateView):

    """Plan detail view"""
    model = Plan
    slug_field = "pk"
    template_name = "plan-detail.html"

    model_for_list = Comment

    form_class = CommentCreateFormDetail

    @property
    def object_list(self):
        object_list = self.model_for_list.objects.filter(
            plan=self.get_object(),
        )
        return object_list.order_by('-id')

    def get_success_url(self):
        messages.success(
            self.request, _(
                "%s succesfully created" %
                self.form_class._meta.model.__name__))
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(PlanDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        form = None
        if self.request.user.__class__.__name__ not in [u'AnonymousUser']:
            form = self.get_form_class()
        context.update({
            'form': form,
        })
        context.update({
            'object_list': self.object_list,
        })
        return context

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.plan = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super(PlanDetailView, self).form_valid(form)


def login(request):
    login_form = LoginForm()

    redirect_url = '/'
    redirect_url = request.GET.get('next') or redirect_url

    if request.method == 'POST' and 'login_form' in request.POST:
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            return login_form.login(request, redirect_url=redirect_url)

    return render(request, "login.html", {
        "login_form": login_form,
    })


def register(request):
    signup_form_user = SignUpUserForm(prefix="user", request=request)

    redirect_url = '/'
    redirect_url = request.GET.get('next') or redirect_url

    if request.method == 'POST' and 'signup_user_form' in request.POST:
        signup_form_user = SignUpUserForm(
            request.POST,
            prefix="user",
            request=request)

        if signup_form_user.is_valid():
            user = signup_form_user.save(request)
            return complete_signup(
                request,
                user,
                EMAIL_VERIFICATION,
                redirect_url)

    return render(request, "register.html", {
        "signup_form_user": signup_form_user,
    })
