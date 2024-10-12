from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer

# Home view
def home(request):
    return redirect('loginn')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('loginn')

# Login view
def loginn(request):
    if request.method == "POST":
        username = request.POST.get('userID')
        password = request.POST.get('password')
        if username.startswith('u_'):
            user = authenticate(request, username=username, password=password)
            if user is not None and not user.is_superuser:
                login(request, user)
                return redirect('user_dashboard')
            else:
                messages.error(request, "Invalid credentials or superuser login attempted")
        else:
            messages.error(request, "Invalid username format")
    return render(request, 'login.html')

# User dashboard view
@login_required
def user_dashboard(request):
    user = request.user
    assigned_projects = user.projects.all()  # Fetch assigned projects
    project_client_info = [{'project_name': project.project_name, 'client_name': project.client.client_name} for project in assigned_projects]
    return render(request, 'UserLogin.html', {'user': user, 'projects': project_client_info})







# Client views
class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

# Project views
class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

# Create project for a specific client and assign users
class ProjectCreateForClientView(generics.GenericAPIView):
    serializer_class = ProjectSerializer

    def post(self, request, id):
        client = get_object_or_404(Client, id=id)
        project_name = request.data.get('project_name')
        user_data = request.data.get('users')
        user_ids = [user['id'] for user in user_data]
        users = User.objects.filter(id__in=user_ids)

        if not project_name or not users.exists():
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        project = Project.objects.create(
            project_name=project_name,
            client=client,
            created_by=request.user
        )
        project.users.set(users)

        project_data = {
            'id': project.id,
            'project_name': project.project_name,
            'client': client.client_name,
            'users': [{'id': user.id, 'name': user.username} for user in users],
            'created_at': project.created_at,
            'created_by': project.created_by.username
        }

        return Response(project_data, status=status.HTTP_201_CREATED)
