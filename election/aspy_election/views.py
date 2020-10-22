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
        post = Post.objects.get(pk=idPost)
        post.numberCandidate = post.numberCandidate + 1

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        cand = Candidate.objects.get(matricule=request["matricule"])
        meta["id"] = cand.id
        meta["status"] = "SUCCESS"
        meta["result"] = serializer.data

        department.save()
        post.save()

        headers = self.get_success_headers(serializer.data)
        return Response(meta, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        meta = {}
        instance = self.get_object()
        
        department = Department.objects.get(pk=instance.department.id)
        department.number = department.number - 1
        post = Post.objects.get(pk=instance.post.id)
        post.numberCandidate = post.numberCandidate - 1

        self.perform_destroy(instance)
        meta["status"] = "SUCCESS"
        
        department.save()
        post.save()

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
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        meta["status"] = "SUCCESS"
        meta["result"] = serializer.data
        
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
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        meta["status"] = "SUCCESS"
        meta["result"] = serializer.data

        candidate.save()
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
        

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        voter = Voter.objects.get(matricule=request["matricule"])
        meta["id"] = voter.id
        meta["status"] = "SUCCESS"
        meta["result"] = serializer.data

        department.save()
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

        department.save()
        return Response(meta, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        meta = {}
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        idDept = request.data["department"]
        idDept = idDept[idDept.find("department")+11: ]
        idDept = int(idDept.replace("/", ""))

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        meta["status"] = "SUCCESS"
        meta["result"] = serializer.data

        if (idDept != instance.department.id):
            oldDepartment = Department.objects.get(pk=instance.department.id)
            newDepartment = Department.objects.get(pk=idDept)

            oldDepartment.number = oldDepartment.number - 1
            newDepartment.number = newDepartment.number + 1
            oldDepartment.save()
            newDepartment.save()

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

@api_view(['GET', 'POST'])
def login(request):

    if (("matricule" not in request.data) or ("email" not in request.data)):
        result = {
            "code": "HTTP_400_BAD_REQUEST",
            "message": "Only matricule and email attributes are accepted",
            "status": "FAILURE",
        }
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
    if (request.method=='POST'):
        matricule = request.data["matricule"]
        email = request.data["email"]

        voter = None
        try:
            voter = Voter.objects.get(matricule=matricule, email=email)
            result = {
                "code": "HTTP_200_OK",
                "login": "SUCCESS",
                "name": voter.name + " " + voter.surename,
                "id": voter.id
            }
            return Response(result, status=status.HTTP_200_OK)
        except:
            result = {
                "code": "HTTP_401_UNAUTHORIZED",
                "login": "FAILED",
            }
            return Response(result)
        
