from django.shortcuts import render
from rest_framework import generics
from .models import ProfilePic, BlogPost, TextPost,ResearchPost
from .serializers import ProfilePicSerializer, BlogPostModelSerializer, TextPostSerializer, ResearchPostModelSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes,authentication_classes


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication]) 
def create_profile_pic(request):
    image_file = request.FILES.get('image_data')

    if image_file:
        # Read binary data from the uploaded image file
        binary_data = image_file.read()

        # Save the image data directly to the database
        profile_pic = ProfilePic(image_data=binary_data)
        profile_pic.save()

        return Response({'message': 'Image saved successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'No image file found in the request'}, status=status.HTTP_400_BAD_REQUEST)


# API endpoint for getting all ProfilePics
@api_view(['GET'])
def get_all_profile_pics(request):
    profile_pics = ProfilePic.objects.all()
    serializer = ProfilePicSerializer(profile_pics, many=True)
    return Response(serializer.data)

# API endpoint for deleting a ProfilePic by primary key
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication]) 
def delete_profile_pic(request, pk):
    try:
        profile_pic = ProfilePic.objects.get(pk=pk)
    except ProfilePic.DoesNotExist:
        return Response({"detail": "ProfilePic not found."}, status=404)
    
    profile_pic.delete()
    return Response(status=204)



# BlogPost CRUD operations
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication]) 
def create_blog_post(request):
    title = request.data.get('title')
    content = request.data.get('content')
    image_file = request.FILES.get('image')

    if title is None or content is None or image_file is None:
        return Response({'error': 'Title, content, and image_data are required fields'}, status=400)
        # Read binary data from the uploaded image file
        
    try:
        # Convert base64 image data to binary
        binary_data = image_file.read()

        # Create BlogPost instance and save
        blog_post = BlogPost.objects.create(title=title, content=content, image=binary_data)

        return Response({'message': 'Blog post created successfully'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def get_all_blog_posts(request):
    blog_posts = BlogPost.objects.all()
    serializer = BlogPostModelSerializer(blog_posts, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication]) 
def delete_blog_post(request, pk):
    try:
        blog_post = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response({"detail": "BlogPost not found."}, status=404)
    
    blog_post.delete()
    return Response(status=204)


# ResearchPost CRUD operations
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication]) 
def create_research_post(request):
    title = request.data.get('title')
    content = request.data.get('content')
    image_file = request.FILES.get('image')

    if title is None or content is None or image_file is None:
        return Response({'error': 'Title, content, and image_data are required fields'}, status=400)
        # Read binary data from the uploaded image file
        
    try:
        # Convert base64 image data to binary
        binary_data = image_file.read()

        # Create BlogPost instance and save
        reasrch_post = ResearchPost.objects.create(title=title, content=content, image=binary_data)

        return Response({'message': 'Research Post created successfully'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def get_all_research_posts(request):
    research_posts = ResearchPost.objects.all()
    serializer = ResearchPostModelSerializer(research_posts, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication]) 
def delete_research_post(request, pk):
    try:
        research_post = ResearchPost.objects.get(pk=pk)
    except ResearchPost.DoesNotExist:
        return Response({"detail": "ResearchPost not found."}, status=404)
    
    research_post.delete()
    return Response(status=204)


# TextPost CRUD operations
@api_view(['POST'])
def create_text_post(request):
    serializer = TextPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_all_text_posts(request):
    text_posts = TextPost.objects.all()
    serializer = TextPostSerializer(text_posts, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication]) 
def delete_text_post(request, pk):
    try:
        text_post = TextPost.objects.get(pk=pk)
    except TextPost.DoesNotExist:
        return Response({"detail": "TextPost not found."}, status=404)
    
    text_post.delete()
    return Response(status=204)

class SuperuserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    