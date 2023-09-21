from rest_framework import viewsets
from .models import WorkflowDefinition, TaskDefinition, WorkflowInstance, TaskInstance
from .serializers import WorkflowDefinitionSerializer, TaskDefinitionSerializer, WorkflowInstanceSerializer, TaskInstanceSerializer

class WorkflowDefinitionViewSet(viewsets.ModelViewSet):
    queryset = WorkflowDefinition.objects.all()
    serializer_class = WorkflowDefinitionSerializer

class TaskDefinitionViewSet(viewsets.ModelViewSet):
    queryset = TaskDefinition.objects.all()
    serializer_class = TaskDefinitionSerializer

class WorkflowInstanceViewSet(viewsets.ModelViewSet):
    queryset = WorkflowInstance.objects.all()
    serializer_class = WorkflowInstanceSerializer

class TaskInstanceViewSet(viewsets.ModelViewSet):
    queryset = TaskInstance.objects.all()
    serializer_class = TaskInstanceSerializer
