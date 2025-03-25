from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Task, User
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    AssignTaskSerializer,
    UserSerializer,
)
from .permissions import IsManagerOrReadOnly

# Create your views here.

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]


    def get_serializer_class(self):
        if self.action in ["create", 'update' ,"partial_update"]:
           return TaskCreateSerializer
        return TaskSerializer 
    

    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)

    @action(detail=True, methods=["post"], serializer_class=AssignTaskSerializer)
    def assign(self,request, pk= None):
        task = self.get_object()
        if request.user.role != 'manager':
            return Response(
               {"error": "Only managers can assign tasks"},
                status=status.HTTP_403_FORBIDDEN ,)
            

        serializer = AssignTaskSerializer(task , data= request.data , partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Task successfully assigned"} , status = status.HTTP_202_ACCEPTED )
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST )
        

    @action(detail=False, methods=["get"], url_path="user/(?P<user_id>[^/.]+)/tasks")
    def user_tasks(self, request, user_id= None):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({'error':'User not found'} , status= status.HTTP_404_NOT_FOUND )

        if request.user.role != "manager" and request.user.id != int(user_id):
            return Response(
                {"error": "You are not allowed to view tasks of another user"},
                status=status.HTTP_403_FORBIDDEN,
            )



        tasks = user.tasks.all()
        serializer = TaskSerializer(tasks , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK )