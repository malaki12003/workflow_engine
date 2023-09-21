from rest_framework import serializers
from .models import WorkflowDefinition, TaskDefinition, WorkflowInstance, Context

class WorkflowDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowDefinition
        fields = '__all__'

class TaskDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDefinition
        fields = '__all__'

class ContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Context
        fields = '__all__'

class WorkflowInstanceSerializer(serializers.ModelSerializer):
    context = ContextSerializer(read_only=True)

    class Meta:
        model = WorkflowInstance
        fields = '__all__'
