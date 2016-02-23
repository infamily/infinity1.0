from core.models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        data = {}
        request = self.context.get('request', None)
        data.update(validated_data)
        data.update({'user': request.user})
        instance = Comment.objects.create(**data)
        return instance

    class Meta:
        model = Comment
        fields = ('text', 'content_type', 'object_id', 'user')
        read_only_fields = ('user', )
