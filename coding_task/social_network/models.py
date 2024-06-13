from django.db import models
import uuid

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_num = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=500, blank=True)
    followers = models.ManyToManyField('self', through='Follow', related_name='following', symmetrical=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    follower = models.ForeignKey(User, related_name='follows', on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name='followed_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

class Discussion(models.Model):
    discussion_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions')
    title_of_post = models.CharField(max_length=255)
    text_field = models.TextField()
    image = models.ImageField(upload_to='discussion_images/', null=True, blank=True)
    hashtags = models.CharField(max_length=255) 
    created_on = models.DateTimeField(auto_now_add=True)
    total_comments = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)


class Comment(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')