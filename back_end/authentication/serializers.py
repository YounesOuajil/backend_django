from rest_framework import serializers
from .models import User, Candidate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')

class CandidateSerializer(UserSerializer):
    class Meta:
        model = Candidate
        fields = UserSerializer.Meta.fields + ('cv', 'cover_letter')
