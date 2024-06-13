from rest_framework import serializers
from .models import User, Discussion, Comment, Follow
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    following = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'name', 'email', 'phone_num', 'password', 'created_on', 'followers', 'following']

    def create(self, validated_data):
        user = User(phone_num=validated_data['phone_num'],name=validated_data['name'],email=validated_data['email'])
        user.password = make_password(validated_data['password'])
        user.save()
        return user 

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name', 'followers', 'following']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followee', 'created_on']

class DiscussionSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Discussion
        fields = ['discussion_id', 'user', 'title_of_post', 'text_field', 'image', 'hashtags', 'created_on', 'total_comments', 'view_count', 'likes' ]

class CommentSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Comment
        fields = ['comment_id', 'user', 'discussion', 'text', 'created_on', 'parent_comment', 'likes']

class DiscussionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = ['discussion_id', 'user', 'title_of_post', 'text_field', 'image', 'hashtags']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_id', 'user', 'discussion', 'text', 'parent_comment']
