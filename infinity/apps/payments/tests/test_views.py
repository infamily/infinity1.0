from django.core.urlresolvers import reverse
from django.utils import formats

from django_webtest import WebTest
from webtest import Upload
from model_mommy import mommy
from allauth.account.models import EmailAddress

from core.models import (
    Comment,
    Article,
    Transaction,
    User,
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
        form['text'] = comment.text
        if comment.article:
            form['article'] = comment.article.pk
        form.submit()

        comment_created = Comment.objects.latest('id')

        self.assertEqual(
            comment_created.text,
            comment.text
        )

        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        form = resp.form
        form['text'] = comment.text
        if comment.article:
            form['article'] = comment.article.pk
        form.submit()

        comment_created = Comment.objects.latest('id')

        self.assertEqual(
            comment_created.text,
            comment.text
        )

        self.logout()


class ArticleTest(WebTest, AuthTestMixin):

    def test_list(self):
        """Create list of Article in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        article_list = []
        article = mommy.make('core.Article', _fill_optional=True)
        article_list.append(article)

        url = reverse('article-list')

        article_list = []
        article = mommy.make('core.Article', _fill_optional=True)
        article_list.append(article)

        url = reverse('article-list')

        url = reverse('article-list')
        resp = self.app.get(url)

        for article in article_list:
            self.assertContains(resp, article.content)

        article_list = []
        article = mommy.make('core.Article', _fill_optional=True)
        article_list.append(article)

        url = reverse('article-list')

        self.login(self.user.email, 'test')

        url = reverse('article-list')
        resp = self.app.get(url)

        for article in article_list:
            self.assertContains(resp, article.content)

        self.logout()

    def test_detail(self):
        """Create Article in database,
        open detail view and
        check that selected fields are visible
        """
        self.init_users()

        article = mommy.make('core.Article', _fill_optional=True)
        url = reverse('article-detail', args=(article.pk,))

        article = mommy.make('core.Article', _fill_optional=True)
        url = reverse('article-detail', args=(article.pk,))

        resp = self.app.get(url)
        self.assertContains(resp, article.content)

        article = mommy.make('core.Article', _fill_optional=True)
        url = reverse('article-detail', args=(article.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        self.assertContains(resp, article.content)

        self.logout()


class TransactionTest(WebTest, AuthTestMixin):

    def test_create(self):
        """Create Transaction object using view
        Check database for created object
        """
        self.init_users()

        transaction = mommy.make('core.Transaction', _fill_optional=True)

        url = reverse('transaction-create', kwargs={
        })

        resp = self.app.get(url)

        form = resp.form
        if transaction.comment:
            form['comment'] = transaction.comment.pk
        form['currency_id'] = transaction.currency_id
        if transaction.sender:
            form['sender'] = transaction.sender.pk
        form['micros'] = transaction.micros
        form['platform_id'] = transaction.platform_id
        form['transaction_external_id'] = transaction.transaction_external_id
        form['amount'] = transaction.amount
        if transaction.recipient:
            form['recipient'] = transaction.recipient.pk
        form.submit()

        transaction_created = Transaction.objects.latest('id')

        self.assertEqual(
            transaction_created.currency_id,
            transaction.currency_id
        )
        self.assertEqual(
            transaction_created.micros,
            transaction.micros
        )
        self.assertEqual(
            transaction_created.platform_id,
            transaction.platform_id
        )
        self.assertEqual(
            transaction_created.transaction_external_id,
            transaction.transaction_external_id
        )
        self.assertEqual(
            transaction_created.amount,
            transaction.amount
        )

        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        form = resp.form
        if transaction.comment:
            form['comment'] = transaction.comment.pk
        form['currency_id'] = transaction.currency_id
        if transaction.sender:
            form['sender'] = transaction.sender.pk
        form['micros'] = transaction.micros
        form['platform_id'] = transaction.platform_id
        form['transaction_external_id'] = transaction.transaction_external_id
        form['amount'] = transaction.amount
        if transaction.recipient:
            form['recipient'] = transaction.recipient.pk
        form.submit()

        transaction_created = Transaction.objects.latest('id')

        self.assertEqual(
            transaction_created.currency_id,
            transaction.currency_id
        )
        self.assertEqual(
            transaction_created.micros,
            transaction.micros
        )
        self.assertEqual(
            transaction_created.platform_id,
            transaction.platform_id
        )
        self.assertEqual(
            transaction_created.transaction_external_id,
            transaction.transaction_external_id
        )
        self.assertEqual(
            transaction_created.amount,
            transaction.amount
        )

        self.logout()
