from rest_framework import viewsets, generics, pagination, response, authentication, permissions 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Post

from post import serializers


class PostPagination(pagination.PageNumberPagination):
    """Get 2 posts in a page"""
    page_size = 2

    def get_paginated_response(self, data):
        return response.Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data,
            'page_size': self.page_size,
            'range_first': (self.page.number * self.page_size) - (self.page_size) + 1,
            'range_last': min((self.page.number * self.page_size), self.page.paginator.count),
        })


class PostViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Posts"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PostSerializer
    queryset = Post.objects.order_by('-created_at')
    pagination_class = PostPagination

    def perform_create(self, serializer):
        """Create a new Post"""
        serializer.save(user=self.request.user)
    
class PostEditView(generics.RetrieveUpdateDestroyAPIView):
    """Manage the authenticated user"""
    serializer_class = serializers.PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.post