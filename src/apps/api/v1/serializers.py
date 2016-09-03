from django.utils.translation import ugettext as _
from rest_framework import serializers
from core.models import Goal, Idea, Plan, Translation, Language
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import truncatewords_html

from .utils import truncate_markdown
import logging


def get_object_translation(obj, language_code):
    language = Language.objects.get(language_code=language_code)
    content_type = ContentType.objects.get_for_model(obj)
    try:
        translation = Translation.objects.get(language=language, content_type=content_type, object_id=obj.id)
        return translation
    except Exception as e:
        logging.exception('Translation not found. Returning actual object.')
        return obj


class GoalSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    short_content = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    def get_detail_url(self, obj):
        absolute_url = obj.get_absolute_url()
        if hasattr(self.context['request'],'LANGUAGE_CODE'):
            language_code = self.context['request'].LANGUAGE_CODE
            return "%s?lang=%s" % (absolute_url, language_code)
        else:
            return absolute_url

    def get_comments_count(self, obj):
        return _("{count} comments").format(count=obj.comment_count())

    def get_title(self, obj):
        language_code = self.context['request'].LANGUAGE_CODE
        try:
            translation = get_object_translation(obj, language_code)
        except Translation.DoesNotExist:
            return obj.name
        return translation.name

    def get_short_content(self, obj):
        language_code = self.context['request'].LANGUAGE_CODE
        try:
            translation = get_object_translation(obj, language_code)
        except Translation.DoesNotExist:
            return truncate_markdown(obj.reason, 250)
        return truncate_markdown(translation.reason, 250)

    class Meta:
        model = Goal
        fields = [
            'title',
            'created_at',
            'detail_url',
            'comments_count',
            'is_link',
            'is_historical',
            'short_content',
            'id'
        ]


class NestedGoalSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()

    def get_detail_url(self, obj):
        absolute_url = obj.get_absolute_url()
        if hasattr(self.context['request'],'LANGUAGE_CODE'):
            language_code = self.context['request'].LANGUAGE_CODE
            return "%s?lang=%s" % (absolute_url, language_code)
        else:
            return absolute_url

    def get_title(self, obj):
        language_code = self.context['request'].LANGUAGE_CODE
        try:
            translation = get_object_translation(obj, language_code)
        except Translation.DoesNotExist:
            return obj.name
        return translation.name

    class Meta:
        model = Goal
        fields = ['title', 'detail_url']


class NestedIdeaSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()

    def get_title(self, obj):
        language_code = self.context['request'].LANGUAGE_CODE
        translation = get_object_translation(obj, language_code)
        return translation.name

    def get_detail_url(self, obj):
        absolute_url = obj.get_absolute_url()
        if hasattr(self.context['request'],'LANGUAGE_CODE'):
            language_code = self.context['request'].LANGUAGE_CODE
            return "%s?lang=%s" % (absolute_url, language_code)
        else:
            return absolute_url

    class Meta:
        model = Idea
        fields = ['title', 'detail_url']


class IdeaSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    short_content = serializers.SerializerMethodField()
    goal = NestedGoalSerializer(many=True)
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        language_code = self.context['request'].LANGUAGE_CODE
        translation = get_object_translation(obj, language_code)
        return translation.name

    def get_detail_url(self, obj):
        absolute_url = obj.get_absolute_url()
        if hasattr(self.context['request'],'LANGUAGE_CODE'):
            language_code = self.context['request'].LANGUAGE_CODE
            return "%s?lang=%s" % (absolute_url, language_code)
        else:
            return absolute_url

    def get_comments_count(self, obj):
        return _("{count} comments").format(count=obj.comment_count())

    def get_short_content(self, obj):
        language_code = self.context['request'].LANGUAGE_CODE
        translation = get_object_translation(obj, language_code)
        return truncate_markdown(translation.summary, 250)

    class Meta:
        model = Idea
        fields = [
            'detail_url',
            'comments_count',
            'short_content',
            'created_at',
            'id',
            'is_link',
            'is_historical',
            'title',
            'goal',
        ]


class PlanSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    short_content = serializers.SerializerMethodField()
    idea = NestedIdeaSerializer()
    remain_usd = serializers.SerializerMethodField()
    usd = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        language_code = self.context['request'].LANGUAGE_CODE
        translation = get_object_translation(obj, language_code)
        return translation.name

    def get_remain_usd(self, obj):
        return obj.get_remain_usd()

    def get_usd(self, obj):
        return obj.get_usd()

    def get_detail_url(self, obj):
        absolute_url = obj.get_absolute_url()
        if hasattr(self.context['request'],'LANGUAGE_CODE'):
            language_code = self.context['request'].LANGUAGE_CODE
            return "%s?lang=%s" % (absolute_url, language_code)
        else:
            return absolute_url

    def get_comments_count(self, obj):
        return _("{count} comments").format(count=obj.comment_count())

    def get_short_content(self, obj):
        language_code = self.context['request'].LANGUAGE_CODE
        translation = get_object_translation(obj, language_code)
        return truncate_markdown(translation.deliverable, 250)

    class Meta:
        model = Plan
        fields = [
            'detail_url',
            'comments_count',
            'short_content',
            'created_at',
            'id',
            'is_link',
            'is_historical',
            'title',
            'idea',
            'remain_usd',
            'usd',
            'personal',
        ]
