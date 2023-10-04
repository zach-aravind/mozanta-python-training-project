from rest_framework import serializers

from .models import Category, Comment, Post


class CategoryReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading Category instances.
    """
    class Meta:
        model = Category
        fields = "__all__"


class PostReadSerializer(serializers.ModelSerializer):
    """
     Serializer for reading Post instances.
    """
    author = serializers.CharField(source="author.username", read_only=True)
    categories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

    def get_categories(self, obj):
        categories = list(
            cat.name for cat in obj.categories.get_queryset().only("name")
        )
        return categories


class PostWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Post instances.
    """
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = "__all__"


class CommentReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading comment instances.
    """
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class CommentWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating comment instances.
    """
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = "__all__"
