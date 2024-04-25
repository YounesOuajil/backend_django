from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from authentication.models import Recruiter,Candidate,Application
from authentication.serializers import RecruiterSerializer
from posts.models import Post
from posts.serializers import PostSerializer




@api_view(['POST'])
def create_recruiter(request):
    serializer = RecruiterSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email= serializer.validated_data.get('email')
        # Check if user already exists
        if Recruiter.objects.filter(username=username).exists():
            return Response({'error': 'User with this username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Creating a new user with encrypted password
        user = Recruiter.objects.create_user(username=username,email=email)
        user.set_password(password)
        user.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_recruiters(request):
    recruiters = Recruiter.objects.all()
    serializer = RecruiterSerializer(recruiters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def retrieve_recruiter(request, recruiter_id):
    recruiter = get_object_or_404(Recruiter, pk=recruiter_id)
    serializer = RecruiterSerializer(recruiter)
    return Response(serializer.data)

@api_view(['PUT'])
def update_recruiter(request, recruiter_id):
    recruiter = get_object_or_404(Recruiter, pk=recruiter_id)
    serializer = RecruiterSerializer(recruiter, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_recruiter(request, recruiter_id):
    recruiter = get_object_or_404(Recruiter, pk=recruiter_id)
    recruiter.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)





@api_view(['GET'])
def candidates_applied_to_RHposts(request, recruiter_id): 
    try:
        # Retrieve the recruiter
        recruiter = Recruiter.objects.get(pk=recruiter_id)
        
        # Filter posts associated with the recruiter
        posts = Post.objects.filter(recruiter=recruiter)
        
        # Initialize an empty list to store candidate data
        candidate_data = []
        
        # Iterate through each post and retrieve candidates who applied
        for post in posts:
            # Retrieve applications for the current post
            applications = Application.objects.filter(post=post)
            
            # Iterate through each application and extract candidate data
            for application in applications:
                candidate_data.append({
                    'candidate_id': application.candidate.id,
                    'application_date': application.date,
                    'post_id': application.post.id,
                })
        
        return Response(candidate_data)
        
    except Recruiter.DoesNotExist:
        return Response({'error': 'Recruiter not found'}, status=status.HTTP_404_NOT_FOUND)
    except Post.DoesNotExist:
        return Response({'error': 'No posts found for this recruiter'}, status=status.HTTP_404_NOT_FOUND)