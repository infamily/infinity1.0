from rest_framework import viewsets
from api.v1.serializers import CommentSerializer
from core.models import Comment


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
