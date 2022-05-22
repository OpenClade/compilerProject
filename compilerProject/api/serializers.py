# import serializers
from rest_framework import serializers
from main.models import * 
from user.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProgrammingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingTask
        fields = "__all__"
        extra_kwargs = {'created_by': {'read_only': True}}


class ProgrammingTaskSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingTaskSolution
        fields = ("id", "task", "author", "language", "code", "is_public", "created_at")
        extra_kwargs = {'author': {'read_only': True}}

