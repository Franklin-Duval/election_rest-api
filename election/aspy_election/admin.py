from django.contrib import admin

from .models import Data, Department, Candidate, Vote, Voter, Post

# Register your models here.
admin.site.register(Data)
admin.site.register(Department)
admin.site.register(Candidate)
admin.site.register(Vote)
admin.site.register(Voter)
admin.site.register(Post)
