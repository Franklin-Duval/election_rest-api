from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Data, Department, Candidate, Vote, Voter, Post
from .serializers import DataSerializer, DepartmentSerializer, CandidateSerializer, VoteSerializer, VoterSerializer, PostSerializer
# Create your views here.

class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def create(self, request, *args, **kwargs):
        meta = {}

        idDept = request.data["department"]
        idDept = idDept[idDept.find("department")+11: ]
        idDept = int(idDept.replace("/", ""))

        idPost = request.data["post"]
        idPost = idPost[idPost.find("post")+4: ]
        idPost = int(idPost.replace("/", ""))

        department = Department.objects.get(pk=idDept)
        department.number = department.number + 1
        department.save()
        post = Post.objects.get(pk=idPost)
        post.numberCandidate = post.numberCandidate + 1
        post.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        meta["status"] = "SUCCESS"
        meta["result"] = serializer.data

        headers = self.get_success_headers(serializer.data)
        return Response(meta, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        meta = {}
        instance = self.get_object()
        
        department = Department.objects.get(pk=instance.department.id)
        department.number = department.number - 1
        department.save()
        post = Post.objects.get(pk=instance.post.id)
        post.numberCandidate = post.numberCandidate - 1
        post.save()

        self.perform_destroy(instance)
        meta["status"] = "SUCCESS"
        return Response(meta, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        meta = {}
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        idDept = request.data["department"]
        idDept = idDept[idDept.find("department")+11: ]
        idDept = int(idDept.replace("/", ""))

        idPost = request.data["post"]
        idPost = idPost[idPost.find("post")+4: ]
        idPost = int(idPost.replace("/", ""))

        if (idDept != instance.department.id):
            oldDepartment = Department.objects.get(pk=instance.department.id)
            newDepartment = Department.objects.get(pk=idDept)

            oldDepartment.number = oldDepartment.number - 1
            newDepartment.number = newDepartment.number + 1
            oldDepartment.save()
            newDepartment.save()

        if (idPost != instance.post.id):
            oldPost = Post.objects.get(pk=instance.post.id)
            newPost = Post.objects.get(pk=idPost)

            oldPost.number = oldPost.number - 1
            newPost.number = newPost.number + 1
            oldPost.save()
            newPost.save()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        meta["status"] = "SUCCESS"
        meta["result"] = serializer.data
        return Response(meta)
    
class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request, *args, **kwargs):
        meta = {}

        idCand = request.data["candidate"]
        idCand = idCand[idCand.find("candidate")+9: ]
        idCand = int(idCand.replace("/", ""))

        candidate = Candidate.objects.get(pk=idCand)
        candidate.numberVotes = candidate.numberVotes + 1
        candidate.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        meta["status"] = "SUCCESS"
        meta["result"] = serializer.data
        headers = self.get_success_headers(serializer.data)
        return Response(meta, status=status.HTTP_201_CREATED, headers=headers)


class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer

    def create(self, request, *args, **kwargs):
        meta = {}

        #we increase the number of students in a given department
        idDept = request.data["department"]
        idDept = idDept[idDept.find("department")+11: ]
        idDept = int(idDept.replace("/", ""))
        department = Department.objects.get(pk=idDept)
        department.number = department.number + 1
        department.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        meta["status"] = "SUCCESS"
        meta["result"] = serializer.data

        headers = self.get_success_headers(serializer.data)
        return Response(meta, status=status.HTTP_201_CREATED, headers=headers)


    def destroy(self, request, *args, **kwargs):
        meta = {}
        instance = self.get_object()
        
        department = Department.objects.get(pk=instance.department.id)
        department.number = department.number - 1
        department.save()

        self.perform_destroy(instance)
        meta["status"] = "SUCCESS"
        return Response(meta, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        meta = {}
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        idDept = request.data["department"]
        idDept = idDept[idDept.find("department")+11: ]
        idDept = int(idDept.replace("/", ""))

        if (idDept != instance.department.id):
            oldDepartment = Department.objects.get(pk=instance.department.id)
            newDepartment = Department.objects.get(pk=idDept)

            oldDepartment.number = oldDepartment.number - 1
            newDepartment.number = newDepartment.number + 1
            oldDepartment.save()
            newDepartment.save()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        meta["status"] = "SUCCESS"
        meta["result"] = serializer.data
        return Response(meta)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

@api_view(['GET'])
def errorPage(request):
    
    result = {
        "code": "HTTP_404_NOT_FOUND",
        "status": "Page not found",
        "message": "Vérifiez votre URL"
    }

    return Response(result, status=status.HTTP_404_NOT_FOUND)

