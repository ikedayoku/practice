from rest_framework import serializers

from core.models import Post
from user.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post objects"""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'content', 'created_at', 'is_completed')
        read_only_fields = ('id', 'user',)
    
    