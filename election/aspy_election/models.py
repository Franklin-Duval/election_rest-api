from django.db import models

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=50)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=100)
    numberCandidate = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Voter(models.Model):
    LEVELS = (
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
        (4, 'Level 4'),
        (5, 'Level 5'),
    )
    matricule = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    surename = models.CharField(max_length=100)
    contact = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)
    level = models.IntegerField(choices=LEVELS)
    date = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name + " " + self.surename + " " +  str(self.level) + " " +  self.department.name


class Candidate(Voter):
    speech = models.TextField(null=True)
    image = models.ImageField(null=True)
    numberVotes = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name + " " + self.surename + " " +  str(self.level) + " " +  self.department.name


class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, null=True, related_name="voter")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, related_name="candidate")
    date = models.DateTimeField(auto_now_add=True)


class Data(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

