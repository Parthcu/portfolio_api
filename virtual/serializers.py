from rest_framework import serializers
from .models import ProfilePic, BlogPost, TextPost,ResearchPost
from django.conf import settings


class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePic
        fields = ['id', 'image_data','created_at']
    
class BlogPostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id','title','content','image','created_at']

class ResearchPostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchPost
        fields = ['id','title','content','image','created_at']

class TextPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextPost
        fields = ['id','title', 'email', 'content','created_at']
        
class BulkEmailSerializer(serializers.Serializer):
    receiver_emails = serializers.ListField(child=serializers.EmailField())
    subject = serializers.CharField()
    body = serializers.CharField()
        
        