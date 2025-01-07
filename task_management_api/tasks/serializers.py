from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task
from django.utils.timezone import now

# Tasks MAnagement (CRUD)
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user', 'completed_at']

    def validate_due_date(self, value):
        if value < now().date():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    def validate_priority(self, value):
        if value not in ['Low', 'Medium', 'High']:
            raise serializers.ValidationError("Invalid priority level.")
        return value
    
# Users Management (CRUD)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
