from django.db.models import fields
from .models import Aspian, Data, Department, Candidate, Vote, Voter, Post
from rest_framework import serializers, permissions

class DataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Data
        fields = [
            'id',
            'name',
            'value'
        ]
        #permission_classes = [permissions.IsAuthenticated]

class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = [
            'id',
            'name',
            'number'
        ]

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'name',
            'numberCandidate'
        ]

class VoterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Voter
        fields = [
            'id',
            'matricule',
            'name',
            'surename',
            'contact',
            'email',
            'level',
            'date',
            'department'
        ]

class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            'id',
            'matricule',
            'name',
            'surename',
            'contact',
            'email',
            'level',
            'date',
            'department',
            'post',
            'image',
            'speech',
            'numberVotes'
        ]

class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = [
            'voter',
            'candidate',
            'date'
        ]

class AspianSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Aspian
        fields = [
            'id',
            'matricule'
        ]