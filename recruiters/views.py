from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from authentication.models import Recruiter
from authentication.serializers import RecruiterSerializer

@api_view(['POST'])
def create_recruiter(request):
    serializer = RecruiterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
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
