from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from authentication.models import Candidate
from authentication.serializers import CandidateSerializer
from rest_framework import status

# Create a new candidate
@api_view(['POST'])
def create_candidate(request):
    serializer = CandidateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List all candidates
@api_view(['GET'])
def list_candidates(request):
    candidates = Candidate.objects.all()
    serializer = CandidateSerializer(candidates, many=True)
    return Response(serializer.data)

# Read details of a specific candidate
@api_view(['GET'])
def retrieve_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    serializer = CandidateSerializer(candidate)
    return Response(serializer.data)

# Update an existing candidate
@api_view(['PUT'])
def update_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    serializer = CandidateSerializer(candidate, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete an existing candidate
@api_view(['DELETE'])
def delete_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    candidate.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
