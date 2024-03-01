from django.shortcuts import render
from rest_framework import generics
from .models import ProfilePic, BlogPost, TextPost,ResearchPost
from .serializers import ProfilePicSerializer, BlogPostModelSerializer, TextPostSerializer, ResearchPostModelSerializer,BulkEmailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes,authentication_classes
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
def get_all_blog_posts(request, post_id=None):
    if post_id is not None:
        # If post_id is provided, get a single blog post
        try:
            blog_post = BlogPost.objects.get(id=post_id)
            serializer = BlogPostModelSerializer(blog_post)
            return Response(serializer.data)
        except BlogPost.DoesNotExist:
            return Response({"message": "Blog post does not exist"}, status=404)
    else:
        # If post_id is not provided, get all blog posts
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
def get_all_research_posts(request, post_id=None):
    if post_id is not None:
        # If post_id is provided, get a single research post
        try:
            research_post = ResearchPost.objects.get(id=post_id)
            serializer = ResearchPostModelSerializer(research_post)
            return Response(serializer.data)
        except ResearchPost.DoesNotExist:
            return Response({"message": "Research post does not exist"}, status=404)
    else:
        # If post_id is not provided, get all research posts
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
    
@api_view(['POST'])
def send_email(request):
    serializer = BulkEmailSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        sender_email = 'support.acca@cuidol.in'
        password = 'jnxjxjbfxlonnaey'  # Replace with your SMTP password

        subject = data.get("subject")
        body = data.get("body")

        receiver_emails = data.get("receiver_emails", [])

        smtp_server = "smtp.gmail.com"
        port = 465  # Use port 465 for SSL
        context = ssl.create_default_context()

        # List to store emails that failed to send
        failed_emails = []

        for receiver_email in receiver_emails:
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            try:
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
            except Exception as e:
                # Log the exception or add the email to the list of failed emails
                failed_emails.append({"email": receiver_email, "error": str(e)})

        if failed_emails:
            return Response({'message': 'Emails sent with some failures', 'failed_emails': failed_emails}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'Emails sent successfully'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)