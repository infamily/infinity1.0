from django.conf.urls import url
from django.views.generic import RedirectView

from core.views import *


urlpatterns = [
    url(r'^ajax/step-include/$', AjaxStepIncludeView.as_view(), name='ajax_step_include_view'),
    url(r'^ajax/comment-vote/$', AjaxCommentVoteView.as_view(), name='ajax_comment_vote_view'),
    url(r'^ajax/comment-translate/$', AjaxCommentTranslateView.as_view(), name='ajax_comment_translate_view'),
    url(r'^ajax/steps-graph-data/$', AjaxPlanStepsGraphDataView.as_view(), name='get-plan-steps-graph-data'),
    url(
        r'^comment/(?P<slug>.*)/update/$',
        CommentUpdateView.as_view(),
        name="comment-update"
    ),

    url(
        r'^comment/(?P<slug>[a-zA-Z-_0-9]+)/delete/$',
        CommentDeleteView.as_view(),
        name="comment-delete"
    ),

    url(
        r'^need/(?P<slug>[a-zA-Z-_0-9]+)/delete/$',
        NeedDeleteView.as_view(),
        name="need-delete"
    ),
    url(
        r'^need/(?P<slug>.*)/update/$',
        NeedUpdateView.as_view(),
        name="need-update"
    ),
    url(
        r'^need/(?P<slug>[a-zA-Z-_0-9]+)/detail/$',
        NeedDetailView.as_view(),
        name="need-detail"
    ),
    url(
        r'^need-create/$',
        NeedCreateView.as_view(),
        name="need-create"
    ),
    url(
        r'^need-create/(?P<concept_q>\w+)/$',
        NeedCreateView.as_view(),
        name="need-create"
    ),
    url(
        r'^goal/(?P<slug>[a-zA-Z-_0-9]+)/delete/$',
        GoalDeleteView.as_view(),
        name="goal-delete"
    ),
    url(
        r'^goal/(?P<slug>.*)/update/$',
        GoalUpdateView.as_view(),
        name="goal-update"
    ),
    url(
        r'^goal/(?P<slug>[a-zA-Z-_0-9]+)/detail/$',
        GoalDetailView.as_view(),
        name="goal-detail"
    ),
    url(
        r'^goal/list/$',
        GoalListView.as_view(),
        name="goal-list"
    ),
    url(
        r'^goal-create/$',
        GoalCreateView.as_view(),
        name="goal-create"
    ),
    url(
        r'^goal-create/(?P<need_id>\d+)/$',
        GoalCreateView.as_view(),
        name="goal-create"
    ),
    url(
        r'^work/(?P<slug>.*)/update/$',
        WorkUpdateView.as_view(),
        name="work-update"
    ),

    url(
        r'^work-create/(?P<task>.*)/$',
        WorkCreateView.as_view(),
        name="work-create"
    ),
    url(
        r'^work/(?P<slug>[a-zA-Z-_0-9]+)/delete/$',
        WorkDeleteView.as_view(),
        name="work-delete"
    ),

    url(
        r'^work/list/$',
        WorkListView.as_view(),
        name="work-list"
    ),
    url(
        r'^work/(?P<slug>[a-zA-Z-_0-9]+)/detail/$',
        WorkDetailView.as_view(),
        name="work-detail"
    ),
    url(
        r'^idea/(?P<slug>.*)/update/$',
        IdeaUpdateView.as_view(),
        name="idea-update"
    ),
    url(
        r'^idea-create/$',
        IdeaCreateView.as_view(),
        name="idea-create"
    ),
    url(
        r'^idea-create/(?P<goal_id>\d+)/$',
        IdeaCreateView.as_view(),
        name="idea-create"
    ),
    url(
        r'^idea/(?P<slug>[a-zA-Z-_0-9]+)/delete/$',
        IdeaDeleteView.as_view(),
        name="idea-delete"
    ),

    url(
        r'^idea/list/$',
        IdeaListView.as_view(),
        name="idea-list"
    ),
    url(
        r'^idea/(?P<slug>[a-zA-Z-_0-9]+)/detail/$',
        IdeaDetailView.as_view(),
        name="idea-detail"
    ),
    url(
        r'^step/(?P<slug>.*)/update/$',
        StepUpdateView.as_view(),
        name="step-update"
    ),

    url(
        r'^step-create/(?P<plan>.*)/$',
        StepCreateView.as_view(),
        name="step-create"
    ),
    url(
        r'^step/(?P<slug>[a-zA-Z-_0-9]+)/delete/$',
        StepDeleteView.as_view(),
        name="step-delete"
    ),

    url(
        r'^step/list/$',
        StepListView.as_view(),
        name="step-list"
    ),
    url(
        r'^step/(?P<slug>[a-zA-Z-_0-9]+)/detail/$',
        StepDetailView.as_view(),
        name="step-detail"
    ),
    url(
        r'^task/(?P<slug>.*)/update/$',
        TaskUpdateView.as_view(),
        name="task-update"
    ),

    url(
        r'^task-create/(?P<step>.*)/$',
        TaskCreateView.as_view(),
        name="task-create"
    ),
    url(
        r'^task/(?P<slug>[a-zA-Z-_0-9]+)/delete/$',
        TaskDeleteView.as_view(),
        name="task-delete"
    ),

    url(
        r'^task/list/$',
        TaskListView.as_view(),
        name="task-list"
    ),
    url(
        r'^task/(?P<slug>[a-zA-Z-_0-9]+)/detail/$',
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    url(
        r'^definition-create/$',
        DefinitionCreateView.as_view(),
        name="definition-create"
    ),
    url(
        r'^definition/(?P<slug>.*)/update$',
        DefinitionUpdateView.as_view(),
        name="definition-update"
    ),
    url(
        r'^definition/list/$',
        DefinitionListView.as_view(),
        name="definition-list"
    ),
    url(
        r'^definition/(?P<slug>[a-zA-Z-_0-9]+)/detail/$',
        DefinitionDetailView.as_view(),
        name="definition-detail"
    ),
    url(
        r'^plan/(?P<slug>.*)/update/$',
        PlanUpdateView.as_view(),
        name="plan-update"
    ),

    url(
        r'^plan-create/$',
        PlanCreateView.as_view(),
        name="plan-create"
    ),
    url(
        r'^plan-create/(?P<idea_id>\d+)/$',
        PlanCreateView.as_view(),
        name="plan-create"
    ),
    url(
        r'^plan/(?P<slug>[a-zA-Z-_0-9]+)/delete/$',
        PlanDeleteView.as_view(),
        name="plan-delete"
    ),

    url(
        r'^plan/list/$',
        PlanListView.as_view(),
        name="plan-list"
    ),
    url(
        r'^plan/(?P<slug>[a-zA-Z-_0-9]+)/detail/$',
        PlanDetailView.as_view(),
        name="plan-detail"
    ),
    url(
        r'^plan/(?P<slug>[a-zA-Z-_0-9]+)/engage/$',
        PlanEngageView.as_view(),
        name="plan-engage"
    ),

    url(
        r'^translation/create/(?P<model_name>\w+)/(?P<object_id>\d+)/$',
        TranslationCreateView.as_view(),
        name="create-translation"
    ),
    url(
        r'^translation/(?P<slug>.*)/update/$',
        TranslationUpdateView.as_view(),
        name="update-translation"
    ),
    url(
        r'^translation/(?P<slug>[a-zA-Z-_0-9]+)/delete/$',
        TranslationDeleteView.as_view(),
        name="delete-translation"
    ),
    url(
        r'^subscribe/$',
        ContentTypeSubscribeFormView.as_view(),
        name="subscribe"
    ),
    url(
        r'^change-step-priority/$',
        ChangeStepPriorityView.as_view(),
        name='change-step-priority'
    ),
    url(
        r'^heavy_data_idea_chained/$',
        IdeaChainedView.as_view(),
        name="heavy_data_idea_chained"
    ),
    url(
        r'^heavy_data_definition_complete/$',
        heavy_data_definition_complete,
        name="heavy_data_definition_complete"
    ),
    url(r'^n/(?P<id>\d+)/$', RedirectView.as_view(url='/need/%(id)s/detail')),
    url(r'^g/(?P<id>\d+)/$', RedirectView.as_view(url='/goal/%(id)s/detail')),
    url(r'^i/(?P<id>\d+)/$', RedirectView.as_view(url='/idea/%(id)s/detail')),
    url(r'^p/(?P<id>\d+)/$', RedirectView.as_view(url='/plan/%(id)s/detail')),
    url(r'^s/(?P<id>\d+)/$', RedirectView.as_view(url='/step/%(id)s/detail')),
    url(r'^t/(?P<id>\d+)/$', RedirectView.as_view(url='/task/%(id)s/detail')),
    url(r'^w/(?P<id>\d+)/$', RedirectView.as_view(url='/work/%(id)s/detail')),
    url(r'^n/(?P<id>\d+)/(?P<lang>[a-zA-Z-_0-9]+)/$', RedirectView.as_view(url='/need/%(id)s/detail/?lang=%(lang)s')),
    url(r'^g/(?P<id>\d+)/(?P<lang>[a-zA-Z-_0-9]+)/$', RedirectView.as_view(url='/goal/%(id)s/detail/?lang=%(lang)s')),
    url(r'^i/(?P<id>\d+)/(?P<lang>[a-zA-Z-_0-9]+)/$', RedirectView.as_view(url='/idea/%(id)s/detail/?lang=%(lang)s')),
    url(r'^p/(?P<id>\d+)/(?P<lang>[a-zA-Z-_0-9]+)/$', RedirectView.as_view(url='/plan/%(id)s/detail/?lang=%(lang)s')),
    url(r'^s/(?P<id>\d+)/(?P<lang>[a-zA-Z-_0-9]+)/$', RedirectView.as_view(url='/step/%(id)s/detail/?lang=%(lang)s')),
    url(r'^t/(?P<id>\d+)/(?P<lang>[a-zA-Z-_0-9]+)/$', RedirectView.as_view(url='/task/%(id)s/detail/?lang=%(lang)s')),
    url(r'^w/(?P<id>\d+)/(?P<lang>[a-zA-Z-_0-9]+)/$', RedirectView.as_view(url='/work/%(id)s/detail/?lang=%(lang)s')),
]
