from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import BasePermission
from rest_framework.authentication import TokenAuthentication

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.user == request.user


# Tasks Management views
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.none()  # Placeholder
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        task = self.get_object()
        if task.status == 'Completed':
            task.status = 'Pending'
        else:
            task.status = 'Completed'
        task.save()
        return Response({'status': task.status, 'completed_at': task.completed_at}, status=status.HTTP_200_OK)
    # sorting task by due date , priority level
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'priority', 'due_date']
    ordering_fields = ['due_date', 'priority']
    
# User Management views
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

