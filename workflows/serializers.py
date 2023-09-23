from rest_framework import serializers
from .models import WorkflowDefinition, TaskDefinition, WorkflowInstance, Context, TaskInstance, TaskOperation


class WorkflowDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowDefinition
        fields = '__all__'

class TaskDefinitionSerializer(serializers.ModelSerializer):
    dependencies = serializers.StringRelatedField(many=True)
    operation = serializers.ChoiceField(choices=TaskOperation.choices)
    class Meta:
        model = TaskDefinition
        fields = '__all__'

class TaskInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskInstance
        fields = '__all__'
class ContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Context
        fields = '__all__'

class WorkflowInstanceSerializer(serializers.ModelSerializer):
    context = ContextSerializer(read_only=True)
    task_instances = TaskInstanceSerializer(many=True, read_only=True)
    class Meta:
        model = WorkflowInstance
        fields = '__all__'
