from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import WorkflowDefinition, TaskDefinition, WorkflowInstance, Context, TaskInstance
from .serializers import WorkflowDefinitionSerializer, TaskDefinitionSerializer, WorkflowInstanceSerializer, \
    ContextSerializer, TaskInstanceSerializer


class WorkflowDefinitionViewSet(viewsets.ModelViewSet):
    queryset = WorkflowDefinition.objects.all()
    serializer_class = WorkflowDefinitionSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        workflow = WorkflowDefinition.objects.create(name=data['name'], description=data['description'])
        for task in data['tasks']:
            TaskDefinition.objects.create(workflow=workflow, name=task['name'], action=task['action'], url=task['url'])
        serializer = WorkflowDefinitionSerializer(workflow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TaskDefinitionViewSet(viewsets.ModelViewSet):
    queryset = TaskDefinition.objects.all()
    serializer_class = TaskDefinitionSerializer

class WorkflowInstanceViewSet(viewsets.ModelViewSet):
    queryset = WorkflowInstance.objects.all()
    serializer_class = WorkflowInstanceSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        workflow = WorkflowDefinition.objects.get(id=data['workflow_id'])
        instance = WorkflowInstance.objects.create(workflow=workflow, params=data['params'])
        instance.initialize_context()
        instance.execute_workflow()
        serializer = WorkflowInstanceSerializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ContextViewSet(viewsets.ModelViewSet):
    queryset = Context.objects.all()
    serializer_class = ContextSerializer

class TaskInstanceViewSet(viewsets.ModelViewSet):
    queryset = TaskInstance.objects.all()
    serializer_class = TaskInstanceSerializer