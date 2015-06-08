from django.core.urlresolvers import reverse
from django.utils import formats

from django_webtest import WebTest
from webtest import Upload
from model_mommy import mommy
from allauth.account.models import EmailAddress

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


class AuthTestMixin(object):

    def init_users(self):
        # Create User object
        self.user = User.objects.create(email='user@mail.com')
        self.user.set_password('test')
        self.user.save()
        # confirmation - sometimes it's required
        EmailAddress.objects.create(
            user=self.user,
            email='user@mail.com',
            primary=True,
            verified=True
        )

    def login(self, login, password):
        resp = self.app.get(reverse('account_login'))
        form = resp.forms[0]
        form['login'] = login
        form['password'] = password
        form.submit()

    def logout(self):
        resp = self.app.get('/accounts/logout/')


class CommentTest(WebTest, AuthTestMixin):

    def test_list(self):
        """Create list of Comment in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        comment_list = []
        comment = mommy.make('core.Comment', _fill_optional=True)
        comment_list.append(comment)

        url = reverse('comment-list1')

        comment_list = []
        comment = mommy.make(
            'core.Comment',
            user=self.anonymoususer,
            _fill_optional=True)
        comment_list.append(comment)

        url = reverse('comment-list1')

        url = reverse('comment-list1')
        resp = self.app.get(url)

        for comment in comment_list:
            self.assertContains(resp, comment.task or "")
            self.assertContains(resp, comment.goal or "")
            self.assertContains(resp, comment.text)
            pass
            self.assertContains(resp, comment.work or "")
            pass
            self.assertContains(resp, comment.idea or "")
            self.assertContains(resp, comment.step or "")
            self.assertContains(resp, comment.user)
            self.assertContains(resp, comment.plan or "")

        comment_list = []
        comment = mommy.make(
            'core.Comment',
            user=self.user,
            _fill_optional=True)
        comment_list.append(comment)

        url = reverse('comment-list1')

        self.login(self.user.email, 'test')

        url = reverse('comment-list1')
        resp = self.app.get(url)

        for comment in comment_list:
            self.assertContains(resp, comment.task or "")
            self.assertContains(resp, comment.goal or "")
            self.assertContains(resp, comment.text)
            pass
            self.assertContains(resp, comment.work or "")
            pass
            self.assertContains(resp, comment.idea or "")
            self.assertContains(resp, comment.step or "")
            self.assertContains(resp, comment.user)
            self.assertContains(resp, comment.plan or "")

        self.logout()

    def test_udpate(self):
        """Update object using view
        Check database for updated object
        """
        self.init_users()

        comment = mommy.make('core.Comment', _fill_optional=True)

        url = reverse('comment-update', kwargs={
            'slug': comment.pk, })

        comment_compare = mommy.make('core.Comment', _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        if comment_compare.task:
            form['task'] = comment_compare.task.pk
        if comment_compare.goal:
            form['goal'] = comment_compare.goal.pk
        form['text'] = comment_compare.text
        if comment_compare.work:
            form['work'] = comment_compare.work.pk
        if comment_compare.idea:
            form['idea'] = comment_compare.idea.pk
        if comment_compare.step:
            form['step'] = comment_compare.step.pk
        form['user'] = comment_compare.user.pk
        if comment_compare.plan:
            form['plan'] = comment_compare.plan.pk
        form.submit()

        comment_updated = Comment.objects.get(pk=comment.pk)

        self.assertEqual(
            comment_compare.text,
            comment_updated.text
        )

        self.login(self.user.email, 'test')

        comment_compare = mommy.make('core.Comment', _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        if comment_compare.task:
            form['task'] = comment_compare.task.pk
        if comment_compare.goal:
            form['goal'] = comment_compare.goal.pk
        form['text'] = comment_compare.text
        if comment_compare.work:
            form['work'] = comment_compare.work.pk
        if comment_compare.idea:
            form['idea'] = comment_compare.idea.pk
        if comment_compare.step:
            form['step'] = comment_compare.step.pk
        form['user'] = comment_compare.user.pk
        if comment_compare.plan:
            form['plan'] = comment_compare.plan.pk
        form.submit()

        comment_updated = Comment.objects.get(pk=comment.pk)

        self.assertEqual(
            comment_compare.text,
            comment_updated.text
        )

        self.logout()

    def test_delete(self):
        """Create Comment in database,
        open delete view and
        check that object was removed
        """
        self.init_users()

        comment = mommy.make('core.Comment', _fill_optional=True)
        self.assertEqual(Comment.objects.count(), 1)
        url = reverse('comment-delete', args=(comment.pk,))

        Comment.objects.all().delete()

        comment = mommy.make('core.Comment', _fill_optional=True)
        url = reverse('comment-delete', args=(comment.pk,))

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Comment.objects.count(), 0)

        comment = mommy.make('core.Comment', _fill_optional=True)
        url = reverse('comment-delete', args=(comment.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Comment.objects.count(), 0)

        self.logout()

    def test_list(self):
        """Create list of Comment in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        comment_list = []
        comment = mommy.make('core.Comment', _fill_optional=True)
        comment_list.append(comment)

        url = reverse('comment-list2')

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        comment_list = []
        comment = mommy.make('core.Comment', _fill_optional=True)
        comment_list.append(comment)

        url = reverse('comment-list2')

        self.login(self.user.email, 'test')

        url = reverse('comment-list2')
        resp = self.app.get(url)

        for comment in comment_list:
            self.assertContains(resp, comment.task or "")
            self.assertContains(resp, comment.goal or "")
            self.assertContains(resp, comment.text)
            pass
            self.assertContains(resp, comment.work or "")
            pass
            self.assertContains(resp, comment.idea or "")
            self.assertContains(resp, comment.step or "")
            self.assertContains(resp, comment.user)
            self.assertContains(resp, comment.plan or "")

        self.logout()

    def test_create(self):
        """Create Comment object using view
        Check database for created object
        """
        self.init_users()

        comment = mommy.make('core.Comment', _fill_optional=True)

        url = reverse('comment-create', kwargs={
        })

        resp = self.app.get(url)

        form = resp.form
        if comment.task:
            form['task'] = comment.task.pk
        if comment.goal:
            form['goal'] = comment.goal.pk
        form['text'] = comment.text
        if comment.work:
            form['work'] = comment.work.pk
        if comment.idea:
            form['idea'] = comment.idea.pk
        if comment.step:
            form['step'] = comment.step.pk
        if comment.plan:
            form['plan'] = comment.plan.pk
        form.submit()

        comment_created = Comment.objects.latest('id')

        self.assertEqual(
            comment_created.text,
            comment.text
        )

        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        form = resp.form
        if comment.task:
            form['task'] = comment.task.pk
        if comment.goal:
            form['goal'] = comment.goal.pk
        form['text'] = comment.text
        if comment.work:
            form['work'] = comment.work.pk
        if comment.idea:
            form['idea'] = comment.idea.pk
        if comment.step:
            form['step'] = comment.step.pk
        if comment.plan:
            form['plan'] = comment.plan.pk
        form.submit()

        comment_created = Comment.objects.latest('id')

        self.assertEqual(
            comment_created.text,
            comment.text
        )

        self.logout()


class GoalTest(WebTest, AuthTestMixin):

    def test_create(self):
        """Create Goal object using view
        Check database for created object
        """
        self.init_users()

        goal = mommy.make('core.Goal', _fill_optional=True)

        url = reverse('goal-create1', kwargs={
            'need': goal.need.pk,
        })

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        form = resp.form
        form['name'] = goal.name
        form['personal'] = goal.personal
        form['reason'] = goal.reason
        form['quantity'] = goal.quantity
        form.submit()

        goal_created = Goal.objects.latest('id')

        self.assertEqual(
            goal_created.name,
            goal.name
        )
        self.assertEqual(
            goal_created.personal,
            goal.personal
        )
        self.assertEqual(
            goal_created.reason,
            goal.reason
        )
        self.assertEqual(
            goal_created.quantity,
            goal.quantity
        )

        self.logout()

    def test_list(self):
        """Create list of Goal in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        goal_list = []
        goal = mommy.make('core.Goal', _fill_optional=True)
        goal_list.append(goal)

        url = reverse('goal-list1')

        goal_list = []
        goal = mommy.make('core.Goal', _fill_optional=True)
        goal_list.append(goal)

        url = reverse('goal-list1')

        url = reverse('goal-list1')
        resp = self.app.get(url)

        for goal in goal_list:
            self.assertContains(resp, goal.name)
            self.assertContains(resp, goal.personal)
            pass
            pass
            self.assertContains(resp, goal.reason)
            self.assertContains(resp, goal.user)
            self.assertContains(resp, goal.need)
            self.assertContains(resp, goal.quantity)

        goal_list = []
        goal = mommy.make('core.Goal', _fill_optional=True)
        goal_list.append(goal)

        url = reverse('goal-list1')

        self.login(self.user.email, 'test')

        url = reverse('goal-list1')
        resp = self.app.get(url)

        for goal in goal_list:
            self.assertContains(resp, goal.name)
            self.assertContains(resp, goal.personal)
            pass
            pass
            self.assertContains(resp, goal.reason)
            self.assertContains(resp, goal.user)
            self.assertContains(resp, goal.need)
            self.assertContains(resp, goal.quantity)

        self.logout()

    def test_delete(self):
        """Create Goal in database,
        open delete view and
        check that object was removed
        """
        self.init_users()

        goal = mommy.make('core.Goal', _fill_optional=True)
        self.assertEqual(Goal.objects.count(), 1)
        url = reverse('goal-delete', args=(goal.pk,))

        Goal.objects.all().delete()

        goal = mommy.make(
            'core.Goal',
            user=self.anonymoususer,
            _fill_optional=True)
        url = reverse('goal-delete', args=(goal.pk,))

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Goal.objects.count(), 0)

        goal = mommy.make('core.Goal', user=self.user, _fill_optional=True)
        url = reverse('goal-delete', args=(goal.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Goal.objects.count(), 0)

        self.logout()

    def test_udpate(self):
        """Update object using view
        Check database for updated object
        """
        self.init_users()

        goal = mommy.make('core.Goal', _fill_optional=True)

        url = reverse('goal-update', kwargs={
            'slug': goal.pk, })

        goal_compare = mommy.make(
            'core.Goal',
            user=self.anonymoususer,
            _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['name'] = goal_compare.name
        form['personal'] = goal_compare.personal
        form['reason'] = goal_compare.reason
        form['need'] = goal_compare.need.pk
        form['quantity'] = goal_compare.quantity
        form.submit()

        goal_updated = Goal.objects.get(pk=goal.pk)

        self.assertEqual(
            goal_compare.name,
            goal_updated.name
        )
        self.assertEqual(
            goal_compare.personal,
            goal_updated.personal
        )
        self.assertEqual(
            goal_compare.reason,
            goal_updated.reason
        )
        self.assertEqual(
            goal_compare.quantity,
            goal_updated.quantity
        )

        self.login(self.user.email, 'test')

        goal_compare = mommy.make(
            'core.Goal',
            user=self.user,
            _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['name'] = goal_compare.name
        form['personal'] = goal_compare.personal
        form['reason'] = goal_compare.reason
        form['need'] = goal_compare.need.pk
        form['quantity'] = goal_compare.quantity
        form.submit()

        goal_updated = Goal.objects.get(pk=goal.pk)

        self.assertEqual(
            goal_compare.name,
            goal_updated.name
        )
        self.assertEqual(
            goal_compare.personal,
            goal_updated.personal
        )
        self.assertEqual(
            goal_compare.reason,
            goal_updated.reason
        )
        self.assertEqual(
            goal_compare.quantity,
            goal_updated.quantity
        )

        self.logout()

    def test_detail(self):
        """Create Goal in database,
        open detail view and
        check that selected fields are visible
        """
        self.init_users()

        goal = mommy.make('core.Goal', _fill_optional=True)
        url = reverse('goal-detail', args=(goal.pk,))

        goal = mommy.make('core.Goal', _fill_optional=True)
        url = reverse('goal-detail', args=(goal.pk,))

        resp = self.app.get(url)
        self.assertContains(resp, goal.name)

        self.assertContains(resp, goal.personal)

        self.assertContains(resp, goal.reason)

        self.assertContains(resp, goal.user)

        self.assertContains(resp, goal.need)

        self.assertContains(resp, goal.quantity)

        goal = mommy.make('core.Goal', _fill_optional=True)
        url = reverse('goal-detail', args=(goal.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        self.assertContains(resp, goal.name)

        self.assertContains(resp, goal.personal)

        self.assertContains(resp, goal.reason)

        self.assertContains(resp, goal.user)

        self.assertContains(resp, goal.need)

        self.assertContains(resp, goal.quantity)

        self.logout()

    def test_list(self):
        """Create list of Goal in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        goal_list = []
        goal = mommy.make('core.Goal', _fill_optional=True)
        goal_list.append(goal)

        url = reverse('goal-list2')

        goal_list = []
        goal = mommy.make('core.Goal', _fill_optional=True)
        goal_list.append(goal)

        url = reverse('goal-list2')

        url = reverse('goal-list2')
        resp = self.app.get(url)

        for goal in goal_list:
            self.assertContains(resp, goal.name)
            self.assertContains(resp, goal.personal)
            pass
            pass
            self.assertContains(resp, goal.reason)
            self.assertContains(resp, goal.user)
            self.assertContains(resp, goal.need)
            self.assertContains(resp, goal.quantity)

        goal_list = []
        goal = mommy.make('core.Goal', _fill_optional=True)
        goal_list.append(goal)

        url = reverse('goal-list2')

        self.login(self.user.email, 'test')

        url = reverse('goal-list2')
        resp = self.app.get(url)

        for goal in goal_list:
            self.assertContains(resp, goal.name)
            self.assertContains(resp, goal.personal)
            pass
            pass
            self.assertContains(resp, goal.reason)
            self.assertContains(resp, goal.user)
            self.assertContains(resp, goal.need)
            self.assertContains(resp, goal.quantity)

        self.logout()

    def test_create(self):
        """Create Goal object using view
        Check database for created object
        """
        self.init_users()

        goal = mommy.make('core.Goal', _fill_optional=True)

        url = reverse('goal-create2', kwargs={
            'need': goal.need.pk,
        })

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        form = resp.form
        form['name'] = goal.name
        form['personal'] = goal.personal
        form['reason'] = goal.reason
        form['quantity'] = goal.quantity
        form.submit()

        goal_created = Goal.objects.latest('id')

        self.assertEqual(
            goal_created.name,
            goal.name
        )
        self.assertEqual(
            goal_created.personal,
            goal.personal
        )
        self.assertEqual(
            goal_created.reason,
            goal.reason
        )
        self.assertEqual(
            goal_created.quantity,
            goal.quantity
        )

        self.logout()


class WorkTest(WebTest, AuthTestMixin):

    def test_list(self):
        """Create list of Work in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        work_list = []
        work = mommy.make('core.Work', _fill_optional=True)
        work_list.append(work)

        url = reverse('work-list1')

        work_list = []
        work = mommy.make('core.Work', _fill_optional=True)
        work_list.append(work)

        url = reverse('work-list1')

        url = reverse('work-list1')
        resp = self.app.get(url)

        for work in work_list:
            self.assertContains(resp, work.task)
            self.assertContains(resp, work.name)
            self.assertContains(resp, work.url or "")
            pass
            pass
            self.assertContains(resp, work.user)
            self.assertContains(resp, work.file or "")
            self.assertContains(resp, work.parent_work_id or "")
            self.assertContains(resp, work.description)

        work_list = []
        work = mommy.make('core.Work', _fill_optional=True)
        work_list.append(work)

        url = reverse('work-list1')

        self.login(self.user.email, 'test')

        url = reverse('work-list1')
        resp = self.app.get(url)

        for work in work_list:
            self.assertContains(resp, work.task)
            self.assertContains(resp, work.name)
            self.assertContains(resp, work.url or "")
            pass
            pass
            self.assertContains(resp, work.user)
            self.assertContains(resp, work.file or "")
            self.assertContains(resp, work.parent_work_id or "")
            self.assertContains(resp, work.description)

        self.logout()

    def test_udpate(self):
        """Update object using view
        Check database for updated object
        """
        self.init_users()

        work = mommy.make('core.Work', _fill_optional=True)

        url = reverse('work-update', kwargs={
            'slug': work.pk, })

        work_compare = mommy.make(
            'core.Work',
            user=self.anonymoususer,
            _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['task'] = work_compare.task.pk
        form['name'] = work_compare.name
        form['url'] = work_compare.url
        if work.file:
            form['file'] = Upload(work_compare.file.path)
        form['parent_work_id'] = work_compare.parent_work_id
        form['description'] = work_compare.description
        form.submit()

        work_updated = Work.objects.get(pk=work.pk)

        self.assertEqual(
            work_compare.name,
            work_updated.name
        )
        self.assertEqual(
            work_compare.url,
            work_updated.url
        )
        if work.file:
            self.assertEqual(
                file(work_compare.file.path).read(),
                file(work_updated.file.path).read()
            )
        self.assertEqual(
            work_compare.parent_work_id,
            work_updated.parent_work_id
        )
        self.assertEqual(
            work_compare.description,
            work_updated.description
        )

        self.login(self.user.email, 'test')

        work_compare = mommy.make(
            'core.Work',
            user=self.user,
            _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['task'] = work_compare.task.pk
        form['name'] = work_compare.name
        form['url'] = work_compare.url
        if work.file:
            form['file'] = Upload(work_compare.file.path)
        form['parent_work_id'] = work_compare.parent_work_id
        form['description'] = work_compare.description
        form.submit()

        work_updated = Work.objects.get(pk=work.pk)

        self.assertEqual(
            work_compare.name,
            work_updated.name
        )
        self.assertEqual(
            work_compare.url,
            work_updated.url
        )
        if work.file:
            self.assertEqual(
                file(work_compare.file.path).read(),
                file(work_updated.file.path).read()
            )
        self.assertEqual(
            work_compare.parent_work_id,
            work_updated.parent_work_id
        )
        self.assertEqual(
            work_compare.description,
            work_updated.description
        )

        self.logout()

    def test_create(self):
        """Create Work object using view
        Check database for created object
        """
        self.init_users()

        work = mommy.make('core.Work', _fill_optional=True)

        url = reverse('work-create', kwargs={
            'task': work.task.pk,
        })

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        form = resp.form
        form['name'] = work.name
        form['url'] = work.url
        form['file'] = work.file
        if work.file:
            form['file'] = Upload(work.file.path)
        form['parent_work_id'] = work.parent_work_id
        form['description'] = work.description
        form.submit()

        work_created = Work.objects.latest('id')

        self.assertEqual(
            work_created.name,
            work.name
        )
        self.assertEqual(
            work_created.url,
            work.url
        )
        self.assertEqual(
            work_created.parent_work_id,
            work.parent_work_id
        )
        self.assertEqual(
            work_created.description,
            work.description
        )

        self.logout()

    def test_delete(self):
        """Create Work in database,
        open delete view and
        check that object was removed
        """
        self.init_users()

        work = mommy.make('core.Work', _fill_optional=True)
        self.assertEqual(Work.objects.count(), 1)
        url = reverse('work-delete', args=(work.pk,))

        Work.objects.all().delete()

        work = mommy.make(
            'core.Work',
            user=self.anonymoususer,
            _fill_optional=True)
        url = reverse('work-delete', args=(work.pk,))

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Work.objects.count(), 0)

        work = mommy.make('core.Work', user=self.user, _fill_optional=True)
        url = reverse('work-delete', args=(work.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Work.objects.count(), 0)

        self.logout()

    def test_list(self):
        """Create list of Work in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        work_list = []
        work = mommy.make('core.Work', _fill_optional=True)
        work_list.append(work)

        url = reverse('work-list2')

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        work_list = []
        work = mommy.make('core.Work', user=self.user, _fill_optional=True)
        work_list.append(work)

        url = reverse('work-list2')

        self.login(self.user.email, 'test')

        url = reverse('work-list2')
        resp = self.app.get(url)

        for work in work_list:
            self.assertContains(resp, work.task)
            self.assertContains(resp, work.name)
            self.assertContains(resp, work.url or "")
            pass
            pass
            self.assertContains(resp, work.user)
            self.assertContains(resp, work.file or "")
            self.assertContains(resp, work.parent_work_id or "")
            self.assertContains(resp, work.description)

        self.logout()

    def test_detail(self):
        """Create Work in database,
        open detail view and
        check that selected fields are visible
        """
        self.init_users()

        work = mommy.make('core.Work', _fill_optional=True)
        url = reverse('work-detail', args=(work.pk,))

        work = mommy.make('core.Work', _fill_optional=True)
        url = reverse('work-detail', args=(work.pk,))

        resp = self.app.get(url)
        self.assertContains(resp, work.task)

        self.assertContains(resp, work.name)

        self.assertContains(resp, work.url or "")

        self.assertContains(resp, work.user)

        self.assertContains(resp, work.file or "")

        self.assertContains(resp, work.parent_work_id or "")

        self.assertContains(resp, work.description)

        work = mommy.make('core.Work', _fill_optional=True)
        url = reverse('work-detail', args=(work.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        self.assertContains(resp, work.task)

        self.assertContains(resp, work.name)

        self.assertContains(resp, work.url or "")

        self.assertContains(resp, work.user)

        self.assertContains(resp, work.file or "")

        self.assertContains(resp, work.parent_work_id or "")

        self.assertContains(resp, work.description)

        self.logout()


class IdeaTest(WebTest, AuthTestMixin):

    def test_list(self):
        """Create list of Idea in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        idea_list = []
        idea = mommy.make('core.Idea', _fill_optional=True)
        idea_list.append(idea)

        url = reverse('idea-list1')

        idea_list = []
        idea = mommy.make('core.Idea', _fill_optional=True)
        idea_list.append(idea)

        url = reverse('idea-list1')

        url = reverse('idea-list1')
        resp = self.app.get(url)

        for idea in idea_list:
            self.assertContains(resp, idea.description)
            self.assertContains(resp, idea.name)
            pass
            pass
            self.assertContains(resp, idea.summary)
            self.assertContains(resp, idea.user)
            self.assertContains(resp, idea.goal)

        idea_list = []
        idea = mommy.make('core.Idea', _fill_optional=True)
        idea_list.append(idea)

        url = reverse('idea-list1')

        self.login(self.user.email, 'test')

        url = reverse('idea-list1')
        resp = self.app.get(url)

        for idea in idea_list:
            self.assertContains(resp, idea.description)
            self.assertContains(resp, idea.name)
            pass
            pass
            self.assertContains(resp, idea.summary)
            self.assertContains(resp, idea.user)
            self.assertContains(resp, idea.goal)

        self.logout()

    def test_udpate(self):
        """Update object using view
        Check database for updated object
        """
        self.init_users()

        idea = mommy.make('core.Idea', _fill_optional=True)

        url = reverse('idea-update', kwargs={
            'slug': idea.pk, })

        idea_compare = mommy.make(
            'core.Idea',
            user=self.anonymoususer,
            _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['description'] = idea_compare.description
        form['name'] = idea_compare.name
        form['summary'] = idea_compare.summary
        form['goal'] = idea_compare.goal.pk
        form.submit()

        idea_updated = Idea.objects.get(pk=idea.pk)

        self.assertEqual(
            idea_compare.description,
            idea_updated.description
        )
        self.assertEqual(
            idea_compare.name,
            idea_updated.name
        )
        self.assertEqual(
            idea_compare.summary,
            idea_updated.summary
        )

        self.login(self.user.email, 'test')

        idea_compare = mommy.make(
            'core.Idea',
            user=self.user,
            _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['description'] = idea_compare.description
        form['name'] = idea_compare.name
        form['summary'] = idea_compare.summary
        form['goal'] = idea_compare.goal.pk
        form.submit()

        idea_updated = Idea.objects.get(pk=idea.pk)

        self.assertEqual(
            idea_compare.description,
            idea_updated.description
        )
        self.assertEqual(
            idea_compare.name,
            idea_updated.name
        )
        self.assertEqual(
            idea_compare.summary,
            idea_updated.summary
        )

        self.logout()

    def test_create(self):
        """Create Idea object using view
        Check database for created object
        """
        self.init_users()

        idea = mommy.make('core.Idea', _fill_optional=True)

        url = reverse('idea-create', kwargs={
            'goal': idea.goal.pk,
        })

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        form = resp.form
        form['description'] = idea.description
        form['name'] = idea.name
        form['summary'] = idea.summary
        form.submit()

        idea_created = Idea.objects.latest('id')

        self.assertEqual(
            idea_created.description,
            idea.description
        )
        self.assertEqual(
            idea_created.name,
            idea.name
        )
        self.assertEqual(
            idea_created.summary,
            idea.summary
        )

        self.logout()

    def test_delete(self):
        """Create Idea in database,
        open delete view and
        check that object was removed
        """
        self.init_users()

        idea = mommy.make('core.Idea', _fill_optional=True)
        self.assertEqual(Idea.objects.count(), 1)
        url = reverse('idea-delete', args=(idea.pk,))

        Idea.objects.all().delete()

        idea = mommy.make(
            'core.Idea',
            user=self.anonymoususer,
            _fill_optional=True)
        url = reverse('idea-delete', args=(idea.pk,))

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Idea.objects.count(), 0)

        idea = mommy.make('core.Idea', user=self.user, _fill_optional=True)
        url = reverse('idea-delete', args=(idea.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Idea.objects.count(), 0)

        self.logout()

    def test_list(self):
        """Create list of Idea in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        idea_list = []
        idea = mommy.make('core.Idea', _fill_optional=True)
        idea_list.append(idea)

        url = reverse('idea-list2')

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        idea_list = []
        idea = mommy.make('core.Idea', user=self.user, _fill_optional=True)
        idea_list.append(idea)

        url = reverse('idea-list2')

        self.login(self.user.email, 'test')

        url = reverse('idea-list2')
        resp = self.app.get(url)

        for idea in idea_list:
            self.assertContains(resp, idea.description)
            self.assertContains(resp, idea.name)
            pass
            pass
            self.assertContains(resp, idea.summary)
            self.assertContains(resp, idea.user)
            self.assertContains(resp, idea.goal)

        self.logout()

    def test_detail(self):
        """Create Idea in database,
        open detail view and
        check that selected fields are visible
        """
        self.init_users()

        idea = mommy.make('core.Idea', _fill_optional=True)
        url = reverse('idea-detail', args=(idea.pk,))

        idea = mommy.make('core.Idea', _fill_optional=True)
        url = reverse('idea-detail', args=(idea.pk,))

        resp = self.app.get(url)
        self.assertContains(resp, idea.description)

        self.assertContains(resp, idea.name)

        self.assertContains(resp, idea.summary)

        self.assertContains(resp, idea.user)

        self.assertContains(resp, idea.goal)

        idea = mommy.make('core.Idea', _fill_optional=True)
        url = reverse('idea-detail', args=(idea.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        self.assertContains(resp, idea.description)

        self.assertContains(resp, idea.name)

        self.assertContains(resp, idea.summary)

        self.assertContains(resp, idea.user)

        self.assertContains(resp, idea.goal)

        self.logout()


class StepTest(WebTest, AuthTestMixin):

    def test_list(self):
        """Create list of Step in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        step_list = []
        step = mommy.make('core.Step', _fill_optional=True)
        step_list.append(step)

        url = reverse('step-list1')

        step_list = []
        step = mommy.make('core.Step', _fill_optional=True)
        step_list.append(step)

        url = reverse('step-list1')

        url = reverse('step-list1')
        resp = self.app.get(url)

        for step in step_list:
            self.assertContains(resp, step.user)
            self.assertContains(resp, step.name)
            pass
            pass
            self.assertContains(resp, step.deliverables)
            self.assertContains(resp, step.priority)
            self.assertContains(resp, step.plan)
            self.assertContains(resp, step.objective)
            self.assertContains(resp, step.investables)

        step_list = []
        step = mommy.make('core.Step', _fill_optional=True)
        step_list.append(step)

        url = reverse('step-list1')

        self.login(self.user.email, 'test')

        url = reverse('step-list1')
        resp = self.app.get(url)

        for step in step_list:
            self.assertContains(resp, step.user)
            self.assertContains(resp, step.name)
            pass
            pass
            self.assertContains(resp, step.deliverables)
            self.assertContains(resp, step.priority)
            self.assertContains(resp, step.plan)
            self.assertContains(resp, step.objective)
            self.assertContains(resp, step.investables)

        self.logout()

    def test_udpate(self):
        """Update object using view
        Check database for updated object
        """
        self.init_users()

        step = mommy.make('core.Step', _fill_optional=True)

        url = reverse('step-update', kwargs={
            'slug': step.pk, })

        step_compare = mommy.make(
            'core.Step',
            user=self.anonymoususer,
            _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['name'] = step_compare.name
        form['deliverables'] = step_compare.deliverables
        form['priority'] = step_compare.priority
        form['plan'] = step_compare.plan.pk
        form['objective'] = step_compare.objective
        form['investables'] = step_compare.investables
        form.submit()

        step_updated = Step.objects.get(pk=step.pk)

        self.assertEqual(
            step_compare.name,
            step_updated.name
        )
        self.assertEqual(
            step_compare.deliverables,
            step_updated.deliverables
        )
        self.assertEqual(
            step_compare.priority,
            step_updated.priority
        )
        self.assertEqual(
            step_compare.objective,
            step_updated.objective
        )
        self.assertEqual(
            step_compare.investables,
            step_updated.investables
        )

        self.login(self.user.email, 'test')

        step_compare = mommy.make(
            'core.Step',
            user=self.user,
            _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['name'] = step_compare.name
        form['deliverables'] = step_compare.deliverables
        form['priority'] = step_compare.priority
        form['plan'] = step_compare.plan.pk
        form['objective'] = step_compare.objective
        form['investables'] = step_compare.investables
        form.submit()

        step_updated = Step.objects.get(pk=step.pk)

        self.assertEqual(
            step_compare.name,
            step_updated.name
        )
        self.assertEqual(
            step_compare.deliverables,
            step_updated.deliverables
        )
        self.assertEqual(
            step_compare.priority,
            step_updated.priority
        )
        self.assertEqual(
            step_compare.objective,
            step_updated.objective
        )
        self.assertEqual(
            step_compare.investables,
            step_updated.investables
        )

        self.logout()

    def test_create(self):
        """Create Step object using view
        Check database for created object
        """
        self.init_users()

        step = mommy.make('core.Step', _fill_optional=True)

        url = reverse('step-create', kwargs={
            'plan': step.plan.pk,
        })

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        form = resp.form
        form['name'] = step.name
        form['deliverables'] = step.deliverables
        form['priority'] = step.priority
        form['objective'] = step.objective
        form['investables'] = step.investables
        form.submit()

        step_created = Step.objects.latest('id')

        self.assertEqual(
            step_created.name,
            step.name
        )
        self.assertEqual(
            step_created.deliverables,
            step.deliverables
        )
        self.assertEqual(
            step_created.priority,
            step.priority
        )
        self.assertEqual(
            step_created.objective,
            step.objective
        )
        self.assertEqual(
            step_created.investables,
            step.investables
        )

        self.logout()

    def test_delete(self):
        """Create Step in database,
        open delete view and
        check that object was removed
        """
        self.init_users()

        step = mommy.make('core.Step', _fill_optional=True)
        self.assertEqual(Step.objects.count(), 1)
        url = reverse('step-delete', args=(step.pk,))

        Step.objects.all().delete()

        step = mommy.make(
            'core.Step',
            user=self.anonymoususer,
            _fill_optional=True)
        url = reverse('step-delete', args=(step.pk,))

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Step.objects.count(), 0)

        step = mommy.make('core.Step', user=self.user, _fill_optional=True)
        url = reverse('step-delete', args=(step.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Step.objects.count(), 0)

        self.logout()

    def test_list(self):
        """Create list of Step in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        step_list = []
        step = mommy.make('core.Step', _fill_optional=True)
        step_list.append(step)

        url = reverse('step-list2')

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        step_list = []
        step = mommy.make('core.Step', user=self.user, _fill_optional=True)
        step_list.append(step)

        url = reverse('step-list2')

        self.login(self.user.email, 'test')

        url = reverse('step-list2')
        resp = self.app.get(url)

        for step in step_list:
            self.assertContains(resp, step.user)
            self.assertContains(resp, step.name)
            pass
            pass
            self.assertContains(resp, step.deliverables)
            self.assertContains(resp, step.priority)
            self.assertContains(resp, step.plan)
            self.assertContains(resp, step.objective)
            self.assertContains(resp, step.investables)

        self.logout()

    def test_detail(self):
        """Create Step in database,
        open detail view and
        check that selected fields are visible
        """
        self.init_users()

        step = mommy.make('core.Step', _fill_optional=True)
        url = reverse('step-detail', args=(step.pk,))

        step = mommy.make('core.Step', _fill_optional=True)
        url = reverse('step-detail', args=(step.pk,))

        resp = self.app.get(url)
        self.assertContains(resp, step.user)

        self.assertContains(resp, step.name)

        self.assertContains(resp, step.deliverables)

        self.assertContains(resp, step.priority)

        self.assertContains(resp, step.plan)

        self.assertContains(resp, step.objective)

        self.assertContains(resp, step.investables)

        step = mommy.make('core.Step', _fill_optional=True)
        url = reverse('step-detail', args=(step.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        self.assertContains(resp, step.user)

        self.assertContains(resp, step.name)

        self.assertContains(resp, step.deliverables)

        self.assertContains(resp, step.priority)

        self.assertContains(resp, step.plan)

        self.assertContains(resp, step.objective)

        self.assertContains(resp, step.investables)

        self.logout()


class TaskTest(WebTest, AuthTestMixin):

    def test_list(self):
        """Create list of Task in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        task_list = []
        task = mommy.make('core.Task', _fill_optional=True)
        task_list.append(task)

        url = reverse('task-list1')

        task_list = []
        task = mommy.make('core.Task', _fill_optional=True)
        task_list.append(task)

        url = reverse('task-list1')

        url = reverse('task-list1')
        resp = self.app.get(url)

        for task in task_list:
            self.assertContains(resp, task.name)
            pass
            pass
            self.assertContains(resp, task.priority)
            self.assertContains(resp, task.step)
            self.assertContains(resp, task.user)

        task_list = []
        task = mommy.make('core.Task', _fill_optional=True)
        task_list.append(task)

        url = reverse('task-list1')

        self.login(self.user.email, 'test')

        url = reverse('task-list1')
        resp = self.app.get(url)

        for task in task_list:
            self.assertContains(resp, task.name)
            pass
            pass
            self.assertContains(resp, task.priority)
            self.assertContains(resp, task.step)
            self.assertContains(resp, task.user)

        self.logout()

    def test_udpate(self):
        """Update object using view
        Check database for updated object
        """
        self.init_users()

        task = mommy.make('core.Task', _fill_optional=True)

        url = reverse('task-update', kwargs={
            'slug': task.pk, })

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        self.login(self.user.email, 'test')

        task_compare = mommy.make(
            'core.Task',
            user=self.user,
            _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['name'] = task_compare.name
        form['priority'] = task_compare.priority
        form['step'] = task_compare.step.pk
        form.submit()

        task_updated = Task.objects.get(pk=task.pk)

        self.assertEqual(
            task_compare.name,
            task_updated.name
        )
        self.assertEqual(
            task_compare.priority,
            task_updated.priority
        )

        self.logout()

    def test_create(self):
        """Create Task object using view
        Check database for created object
        """
        self.init_users()

        task = mommy.make('core.Task', _fill_optional=True)

        url = reverse('task-create', kwargs={
            'step': task.step.pk,
        })

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        form = resp.form
        form['name'] = task.name
        form['priority'] = task.priority
        form.submit()

        task_created = Task.objects.latest('id')

        self.assertEqual(
            task_created.name,
            task.name
        )
        self.assertEqual(
            task_created.priority,
            task.priority
        )

        self.logout()

    def test_delete(self):
        """Create Task in database,
        open delete view and
        check that object was removed
        """
        self.init_users()

        task = mommy.make('core.Task', _fill_optional=True)
        self.assertEqual(Task.objects.count(), 1)
        url = reverse('task-delete', args=(task.pk,))

        Task.objects.all().delete()

        task = mommy.make(
            'core.Task',
            user=self.anonymoususer,
            _fill_optional=True)
        url = reverse('task-delete', args=(task.pk,))

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Task.objects.count(), 0)

        task = mommy.make('core.Task', user=self.user, _fill_optional=True)
        url = reverse('task-delete', args=(task.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Task.objects.count(), 0)

        self.logout()

    def test_list(self):
        """Create list of Task in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        task_list = []
        task = mommy.make('core.Task', _fill_optional=True)
        task_list.append(task)

        url = reverse('task-list2')

        task_list = []
        task = mommy.make(
            'core.Task',
            user=self.anonymoususer,
            _fill_optional=True)
        task_list.append(task)

        url = reverse('task-list2')

        url = reverse('task-list2')
        resp = self.app.get(url)

        for task in task_list:
            self.assertContains(resp, task.name)
            pass
            pass
            self.assertContains(resp, task.priority)
            self.assertContains(resp, task.step)
            self.assertContains(resp, task.user)

        task_list = []
        task = mommy.make('core.Task', user=self.user, _fill_optional=True)
        task_list.append(task)

        url = reverse('task-list2')

        self.login(self.user.email, 'test')

        url = reverse('task-list2')
        resp = self.app.get(url)

        for task in task_list:
            self.assertContains(resp, task.name)
            pass
            pass
            self.assertContains(resp, task.priority)
            self.assertContains(resp, task.step)
            self.assertContains(resp, task.user)

        self.logout()

    def test_detail(self):
        """Create Task in database,
        open detail view and
        check that selected fields are visible
        """
        self.init_users()

        task = mommy.make('core.Task', _fill_optional=True)
        url = reverse('task-detail', args=(task.pk,))

        task = mommy.make('core.Task', _fill_optional=True)
        url = reverse('task-detail', args=(task.pk,))

        resp = self.app.get(url)
        self.assertContains(resp, task.name)

        self.assertContains(resp, task.priority)

        self.assertContains(resp, task.step)

        self.assertContains(resp, task.user)

        task = mommy.make('core.Task', _fill_optional=True)
        url = reverse('task-detail', args=(task.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        self.assertContains(resp, task.name)

        self.assertContains(resp, task.priority)

        self.assertContains(resp, task.step)

        self.assertContains(resp, task.user)

        self.logout()


class UserTest(WebTest, AuthTestMixin):

    def test_detail(self):
        """Create User in database,
        open detail view and
        check that selected fields are visible
        """
        self.init_users()

        user = mommy.make('core.User', _fill_optional=True)
        url = reverse('user-detail')

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        user = self.user
        url = reverse('user-detail')
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        self.assertContains(resp, user.introduction)

        self.assertContains(resp, user.email)

        self.logout()

    def test_udpate(self):
        """Update object using view
        Check database for updated object
        """
        self.init_users()

        user = mommy.make('core.User', _fill_optional=True)

        url = reverse('user-update', kwargs={
        })

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        self.login(self.user.email, 'test')

        user = self.user
        user_compare = mommy.make('core.User', _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['introduction'] = user_compare.introduction
        form['email'] = user_compare.email
        form.submit()

        user_updated = User.objects.get(pk=user.pk)

        self.assertEqual(
            user_compare.introduction,
            user_updated.introduction
        )
        self.assertEqual(
            user_compare.email,
            user_updated.email
        )

        self.logout()


class NeedTest(WebTest, AuthTestMixin):

    def test_create(self):
        """Create Need object using view
        Check database for created object
        """
        self.init_users()

        need = mommy.make('core.Need', _fill_optional=True)

        url = reverse('need-create', kwargs={
        })

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        form = resp.form
        if need.type:
            form['type'] = need.type.pk
        form['name'] = need.name
        form.submit()

        need_created = Need.objects.latest('id')

        self.assertEqual(
            need_created.name,
            need.name
        )

        self.logout()

    def test_list(self):
        """Create list of Need in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        need_list = []
        need = mommy.make('core.Need', _fill_optional=True)
        need_list.append(need)

        url = reverse('need-list')

        need_list = []
        need = mommy.make('core.Need', _fill_optional=True)
        need_list.append(need)

        url = reverse('need-list')

        url = reverse('need-list')
        resp = self.app.get(url)

        for need in need_list:
            pass
            self.assertContains(resp, need.type or "")
            self.assertContains(resp, need.name)

        need_list = []
        need = mommy.make('core.Need', _fill_optional=True)
        need_list.append(need)

        url = reverse('need-list')

        self.login(self.user.email, 'test')

        url = reverse('need-list')
        resp = self.app.get(url)

        for need in need_list:
            pass
            self.assertContains(resp, need.type or "")
            self.assertContains(resp, need.name)

        self.logout()

    def test_detail(self):
        """Create Need in database,
        open detail view and
        check that selected fields are visible
        """
        self.init_users()

        need = mommy.make('core.Need', _fill_optional=True)
        url = reverse('need-detail', args=(need.pk,))

        need = mommy.make('core.Need', _fill_optional=True)
        url = reverse('need-detail', args=(need.pk,))

        resp = self.app.get(url)

        self.assertContains(resp, need.type or "")

        self.assertContains(resp, need.name)

        need = mommy.make('core.Need', _fill_optional=True)
        url = reverse('need-detail', args=(need.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        self.assertContains(resp, need.type or "")

        self.assertContains(resp, need.name)

        self.logout()


class PlanTest(WebTest, AuthTestMixin):

    def test_list(self):
        """Create list of Plan in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        plan_list = []
        plan = mommy.make('core.Plan', _fill_optional=True)
        plan_list.append(plan)

        url = reverse('plan-list1')

        plan_list = []
        plan = mommy.make('core.Plan', _fill_optional=True)
        plan_list.append(plan)

        url = reverse('plan-list1')

        url = reverse('plan-list1')
        resp = self.app.get(url)

        for plan in plan_list:
            self.assertContains(resp, plan.name)
            pass
            pass
            self.assertContains(resp, plan.idea)
            self.assertContains(resp, plan.deliverable)
            self.assertContains(resp, plan.user)
            self.assertContains(resp, plan.situation)

        plan_list = []
        plan = mommy.make('core.Plan', _fill_optional=True)
        plan_list.append(plan)

        url = reverse('plan-list1')

        self.login(self.user.email, 'test')

        url = reverse('plan-list1')
        resp = self.app.get(url)

        for plan in plan_list:
            self.assertContains(resp, plan.name)
            pass
            pass
            self.assertContains(resp, plan.idea)
            self.assertContains(resp, plan.deliverable)
            self.assertContains(resp, plan.user)
            self.assertContains(resp, plan.situation)

        self.logout()

    def test_udpate(self):
        """Update object using view
        Check database for updated object
        """
        self.init_users()

        plan = mommy.make('core.Plan', _fill_optional=True)

        url = reverse('plan-update', kwargs={
            'slug': plan.pk, })

        plan_compare = mommy.make(
            'core.Plan',
            user=self.anonymoususer,
            _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['name'] = plan_compare.name
        form['idea'] = plan_compare.idea.pk
        form['deliverable'] = plan_compare.deliverable
        form['situation'] = plan_compare.situation
        form.submit()

        plan_updated = Plan.objects.get(pk=plan.pk)

        self.assertEqual(
            plan_compare.name,
            plan_updated.name
        )
        self.assertEqual(
            plan_compare.deliverable,
            plan_updated.deliverable
        )
        self.assertEqual(
            plan_compare.situation,
            plan_updated.situation
        )

        self.login(self.user.email, 'test')

        plan_compare = mommy.make(
            'core.Plan',
            user=self.user,
            _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['name'] = plan_compare.name
        form['idea'] = plan_compare.idea.pk
        form['deliverable'] = plan_compare.deliverable
        form['situation'] = plan_compare.situation
        form.submit()

        plan_updated = Plan.objects.get(pk=plan.pk)

        self.assertEqual(
            plan_compare.name,
            plan_updated.name
        )
        self.assertEqual(
            plan_compare.deliverable,
            plan_updated.deliverable
        )
        self.assertEqual(
            plan_compare.situation,
            plan_updated.situation
        )

        self.logout()

    def test_create(self):
        """Create Plan object using view
        Check database for created object
        """
        self.init_users()

        plan = mommy.make('core.Plan', _fill_optional=True)

        url = reverse('plan-create', kwargs={
            'idea': plan.idea.pk,
        })

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        form = resp.form
        form['name'] = plan.name
        form['deliverable'] = plan.deliverable
        form['situation'] = plan.situation
        form.submit()

        plan_created = Plan.objects.latest('id')

        self.assertEqual(
            plan_created.name,
            plan.name
        )
        self.assertEqual(
            plan_created.deliverable,
            plan.deliverable
        )
        self.assertEqual(
            plan_created.situation,
            plan.situation
        )

        self.logout()

    def test_delete(self):
        """Create Plan in database,
        open delete view and
        check that object was removed
        """
        self.init_users()

        plan = mommy.make('core.Plan', _fill_optional=True)
        self.assertEqual(Plan.objects.count(), 1)
        url = reverse('plan-delete', args=(plan.pk,))

        Plan.objects.all().delete()

        plan = mommy.make(
            'core.Plan',
            user=self.anonymoususer,
            _fill_optional=True)
        url = reverse('plan-delete', args=(plan.pk,))

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Plan.objects.count(), 0)

        plan = mommy.make('core.Plan', user=self.user, _fill_optional=True)
        url = reverse('plan-delete', args=(plan.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Plan.objects.count(), 0)

        self.logout()

    def test_list(self):
        """Create list of Plan in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        plan_list = []
        plan = mommy.make('core.Plan', _fill_optional=True)
        plan_list.append(plan)

        url = reverse('plan-list2')

        plan_list = []
        plan = mommy.make(
            'core.Plan',
            user=self.anonymoususer,
            _fill_optional=True)
        plan_list.append(plan)

        url = reverse('plan-list2')

        url = reverse('plan-list2')
        resp = self.app.get(url)

        for plan in plan_list:
            self.assertContains(resp, plan.name)
            pass
            pass
            self.assertContains(resp, plan.idea)
            self.assertContains(resp, plan.deliverable)
            self.assertContains(resp, plan.user)
            self.assertContains(resp, plan.situation)

        plan_list = []
        plan = mommy.make('core.Plan', user=self.user, _fill_optional=True)
        plan_list.append(plan)

        url = reverse('plan-list2')

        self.login(self.user.email, 'test')

        url = reverse('plan-list2')
        resp = self.app.get(url)

        for plan in plan_list:
            self.assertContains(resp, plan.name)
            pass
            pass
            self.assertContains(resp, plan.idea)
            self.assertContains(resp, plan.deliverable)
            self.assertContains(resp, plan.user)
            self.assertContains(resp, plan.situation)

        self.logout()

    def test_detail(self):
        """Create Plan in database,
        open detail view and
        check that selected fields are visible
        """
        self.init_users()

        plan = mommy.make('core.Plan', _fill_optional=True)
        url = reverse('plan-detail', args=(plan.pk,))

        plan = mommy.make('core.Plan', _fill_optional=True)
        url = reverse('plan-detail', args=(plan.pk,))

        resp = self.app.get(url)
        self.assertContains(resp, plan.name)

        self.assertContains(resp, plan.idea)

        self.assertContains(resp, plan.deliverable)

        self.assertContains(resp, plan.user)

        self.assertContains(resp, plan.situation)

        plan = mommy.make('core.Plan', _fill_optional=True)
        url = reverse('plan-detail', args=(plan.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        self.assertContains(resp, plan.name)

        self.assertContains(resp, plan.idea)

        self.assertContains(resp, plan.deliverable)

        self.assertContains(resp, plan.user)

        self.assertContains(resp, plan.situation)

        self.logout()
