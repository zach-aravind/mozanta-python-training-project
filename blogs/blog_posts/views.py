from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .pagination import BlogListCreatePagination
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

from blog_posts.models import Category, Comment, Post
from blog_posts.serializers import (
    CategoryReadSerializer,
    CommentReadSerializer,
    CommentWriteSerializer,
    PostReadSerializer,
    PostWriteSerializer,
)

from .permissions import IsAuthorOrReadOnly


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoints to get and list the post categories
    """
    queryset = Category.objects.all()
    serializer_class = CategoryReadSerializer
    permission_classes = (permissions.AllowAny,)


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD operations in blogs
    """
    queryset = Post.objects.all()
    pagination_class = BlogListCreatePagination

    @action(detail=False, methods=['GET'])
    def get_user_token(self, request):
        user = self.request.user
        try:
            token = Token.objects.get(user=user)
            return Response({'token': token.key})
        except Token.DoesNotExist:
            return Response({'error': 'Token does not exist for this user.'},
                            status=400)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return PostWriteSerializer

        return PostReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for comments for particular blog.
    """
    queryset = Comment.objects.all()

    def get_queryset(self):
        res = super().get_queryset()
        post_id = self.kwargs.get("post_id")
        return res.filter(post__id=post_id)

    @action(detail=False, methods=['GET'])
    def get_user_token(self, request):
        user = self.request.user
        try:
            token = Token.objects.get(user=user)
            return Response({'token': token.key})
        except Token.DoesNotExist:
            return Response({'error': 'Token does not exist for this user.'},
                            status=400)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return CommentWriteSerializer

        return CommentReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()


class LikePostAPIView(APIView):
    """
    Like the blogs.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        user = request.user
        post = get_object_or_404(Post, pk=pk)

        if user in post.likes.all():
            post.likes.remove(user)

        else:
            post.likes.add(user)

        return Response(status=status.HTTP_200_OK)


class HomePageView(ListView):
    def index(request):
        posts = Post.objects.all()
        p = Paginator(posts, 5)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        context = {'page_obj': page_obj}
        return render(request, 'users/index.html', context)
