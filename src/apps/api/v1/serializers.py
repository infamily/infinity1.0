from rest_framework import serializers
from core.models import Goal, Idea


class GoalSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    short_content = serializers.SerializerMethodField()

    def get_detail_url(self, obj):
        return obj.get_absolute_url()

    def get_comments_count(self, obj):
        return obj.comment_count()

    def get_short_content(self, obj):
        return obj.reason[:34]

    class Meta:
        model = Goal
        fields = [
            'name',
            'language',
            'created_at',
            'detail_url',
            'comments_count',
            'is_link',
            'is_historical',
            'short_content',
            'id'
        ]


class IdeaSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    short_content = serializers.SerializerMethodField()
    goal = GoalSerializer(many=True)

    def get_detail_url(self, obj):
        return obj.get_absolute_url()

    def get_comments_count(self, obj):
        return obj.comment_count()

    def get_short_content(self, obj):
        return obj.description[:34]

    class Meta:
        model = Idea
        fields = [
            'detail_url',
            'comments_count',
            'short_content',
            'language',
            'created_at',
            'id',
            'is_link',
            'is_historical',
            'name',
            'goal',
        ]


class PlanSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    short_content = serializers.SerializerMethodField()
    idea = IdeaSerializer()
    remain_usd = serializers.SerializerMethodField()
    usd = serializers.SerializerMethodField()

    def get_remain_usd(self, obj):
        return obj.get_remain_usd()

    def get_usd(self, obj):
        return obj.get_usd()

    def get_detail_url(self, obj):
        return obj.get_absolute_url()

    def get_comments_count(self, obj):
        return obj.comment_count()

    def get_short_content(self, obj):
        return obj.deliverable[:34]

    class Meta:
        model = Idea
        fields = [
            'detail_url',
            'comments_count',
            'short_content',
            'language',
            'created_at',
            'id',
            'is_link',
            'is_historical',
            'name',
            'idea',
            'remain_usd',
            'usd',
            'personal',
        ]
