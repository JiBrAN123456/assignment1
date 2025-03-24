from rest_framework import serializers
from .models import Task, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' ,'username', 'email', 'role']


class TaskSerializer(serializers.ModelSerializer):
    assigned_users = UserSerializer(many = True , read_only= True)
    created_by = UserSerializer(read_only = True)
    
    
    class Meta:
        model = Task 
        fields = "__all__"       


class TaskCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task           
        fields = [ 'id', 'name' , ' description' , 'status' ] 


    def create(self , validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)   
    

class AssignTaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        many = True


    )    

    class Meta:
        model = Task
        fields = ['id', 'assigned_users']


    def update(self, instance, validated_data):
        users = validated_data.pop('assigned_users',[])    
        instance.assigned_users.set(users)
        return instance