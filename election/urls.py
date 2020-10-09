"""election URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

from .aspy_election import views

routers = routers.DefaultRouter()
routers.register(r'data', views.DataViewSet)
routers.register(r'department', views.DepartmentViewSet)
routers.register(r'candidate', views.CandidateViewSet)
routers.register(r'voter', views.VoterViewSet)
routers.register(r'vote', views.VoteViewSet)
routers.register(r'post', views.PostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(routers.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^[a-zA-Z0-9/,;:!\\*-+^$ù&é(-è_çà)]+/$', views.errorPage)
]
