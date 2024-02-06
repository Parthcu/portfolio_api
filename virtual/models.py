from django.db import models
import base64
# Create your models here.
class ProfilePic(models.Model):
    id = models.AutoField(primary_key=True)
    image_data = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class BlogPost(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class ResearchPost(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
class TextPost(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title