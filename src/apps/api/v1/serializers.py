from rest_framework import serializers
from core.models import Goal


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

        read_only_fields = fields
