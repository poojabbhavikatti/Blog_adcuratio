from django.shortcuts import render
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BlogPost
from .serialisation import BlogPostSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

@login_required
@api_view(['GET'])
def blog_post_list(request):
    blog_posts = BlogPost.objects.all()
    serializer = BlogPostSerializer(blog_posts, many=True)
    return Response(serializer.data)

@login_required
@api_view(['GET'])
def blog_post_detail(request, pk):
    try:
        blog_post = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    serializer = BlogPostSerializer(blog_post)
    return Response(serializer.data)

@login_required
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blog_post_create(request):
    serializer = BlogPostSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def blog_post_update(request, pk):
    try:
        blog_post = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if not blog_post.can_edit(request.user):
        return Response({'error': 'You do not have permission to edit this post.'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = BlogPostSerializer(blog_post, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def blog_post_delete(request, pk):
    try:
        blog_post = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if not blog_post.can_edit(request.user):
        return Response({'error': 'You do not have permission to delete this post.'}, status=status.HTTP_403_FORBIDDEN)
    
    blog_post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@login_required
class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=201)
        return Response(serializer.errors, status=400)


