from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Follow, Discussion, Comment
from .serializers import UserSerializer, UserSearchSerializer,FollowSerializer,DiscussionSerializer,CommentSerializer,DiscussionCreateSerializer,CommentCreateSerializer

@api_view(['POST'])
def user_signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                return Response({'message': 'Authentication successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    serializer = UserSearchSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def update_user(request):
    user_id = request.data.get('user_id')
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request):
    user_id = request.data.get('user_id')
    try:
        user = User.objects.get(user_id=user_id)
        discussions = Discussion.objects.filter(user=user)
        for discussion in discussions:
            discussion.delete()
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def search_users(request):
    name = request.data.get('name', '')
    if not name:
        return Response({"error": "Name query parameter cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
    results = User.objects.filter(Q(name__startswith=name) | Q(name__contains=name)).order_by('name')
    serializer = UserSearchSerializer(results, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_discussion(request):
    serializer = DiscussionCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_discussion(request):
    discussion_id = request.data.get('discussion_id')
    try:
        discussion = Discussion.objects.get(discussion_id=discussion_id)
    except Discussion.DoesNotExist:
        return Response({'error': 'Discussion not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = DiscussionCreateSerializer(discussion, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_discussion(request):
    discussion_id = request.data.get('discussion_id')
    try:
        discussion = Discussion.objects.get(discussion_id=discussion_id)
        discussion.delete()
        return Response({'message': 'Discussion deleted successfully'}, status=status.HTTP_200_OK)
    except Discussion.DoesNotExist:
        return Response({'error': 'Discussion not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_discussions_by_tag(request):
    tags = request.query_params.get('tags', '')
    if not tags:
        discussions = Discussion.objects.all()
        serializer = DiscussionSerializer(discussions, many=True)
        return Response(serializer.data)
    discussions = Discussion.objects.filter(Q(hashtags__startswith=tags) | Q(hashtags__contains=tags)).order_by('-total_comments')
    serializer = DiscussionSerializer(discussions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_discussions_by_text(request):
    text = request.query_params.get('text', '')
    if not text:
        discussions = Discussion.objects.all()
        serializer = DiscussionSerializer(discussions, many=True)
        return Response(serializer.data)
    discussions = Discussion.objects.filter(Q(text_field__startswith=text) | Q(text_field__contains=text)).order_by('-total_comments')
    serializer = DiscussionSerializer(discussions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def follow_user(request):
    if request.method == 'POST':
        follower_id = request.data.get('follower_id')
        followee_id = request.data.get('followee_id')
        try:
            follower = User.objects.get(user_id=follower_id)
            followee = User.objects.get(user_id=followee_id)
            if follower != followee:
                follow, created = Follow.objects.get_or_create(follower=follower, followee=followee)
                if created:
                    return Response({'message': 'Followed successfully'}, status=status.HTTP_201_CREATED)
                return Response({'message': 'Already following'}, status=status.HTTP_200_OK)
            return Response({'error': 'Users cannot follow themselves'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def unfollow_user(request):
    if request.method == 'POST':
        follower_id = request.data.get('follower_id')
        followee_id = request.data.get('followee_id')
        try:
            follower = User.objects.get(user_id=follower_id)
            followee = User.objects.get(user_id=followee_id)
            follow = Follow.objects.get(follower=follower, followee=followee)
            follow.delete()
            return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Follow.DoesNotExist:
            return Response({'error': 'Not following this user'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_comment(request):
    serializer = CommentCreateSerializer(data=request.data)
    if serializer.is_valid():
        comment = serializer.save()
        discussion = comment.discussion
        discussion.total_comments += 1
        discussion.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def like_discussion(request):
    user_id = request.data.get('user_id')
    discussion_id = request.data.get('discussion_id')
    try:
        user = User.objects.get(user_id=user_id)
        discussion = Discussion.objects.get(discussion_id=discussion_id)
        if discussion.likes.filter(user=user).exists():
            discussion.likes.filter(user=user).delete()
            return Response({'message': 'Like removed'}, status=status.HTTP_200_OK)
        else:
            discussion.likes.create(user=user)
            return Response({'message': 'Liked successfully'}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Discussion.DoesNotExist:
        return Response({'error': 'Discussion not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def like_comment(request):
    user_id = request.data.get('user_id')
    comment_id = request.data.get('comment_id')
    try:
        user = User.objects.get(user_id=user_id)
        comment = Comment.objects.get(comment_id=comment_id)
        if comment.likes.filter(user=user).exists():
            comment.likes.filter(user=user).delete()
            return Response({'message': 'Like removed'}, status=status.HTTP_200_OK)
        else:
            comment.likes.create(user=user)
            return Response({'message': 'Liked successfully'}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_comment(request):
    comment_id = request.data.get('comment_id')
    try:
        comment = Comment.objects.get(comment_id=comment_id)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CommentCreateSerializer(comment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_comment(request):
    comment_id = request.data.get('comment_id')
    try:
        comment = Comment.objects.get(comment_id=comment_id)
        comment.delete()
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_discussion_detail(request):
    discussion_id = request.data.get('discussion_id')
    try:
        discussion = Discussion.objects.get(discussion_id=discussion_id)
        discussion.view_count += 1
        discussion.save()
        serializer = DiscussionSerializer(discussion)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Discussion.DoesNotExist:
        return Response({'error': 'Discussion not found'}, status=status.HTTP_404_NOT_FOUND)

