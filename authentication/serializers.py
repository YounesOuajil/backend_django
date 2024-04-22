from rest_framework import serializers
from .models import User, Candidate,Event,Application,Recruiter


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
# class CandidateSerializer(UserSerializer):
#     class Meta:
#         model = Candidate
#         fields = UserSerializer.Meta.fields + ('cv', 'cover_letter')
from rest_framework import serializers
from .models import Candidate, Event

class CandidateSerializer(serializers.ModelSerializer):
     class Meta:
         model = Candidate
         fields = '__all__'


class RecruiterSerializer(serializers.ModelSerializer):
     class Meta:
         model = Recruiter
         fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'