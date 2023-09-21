from django.db import models

class WorkflowDefinition(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class TaskDefinition(models.Model):
    workflow = models.ForeignKey(WorkflowDefinition, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    priority = models.IntegerField()

class WorkflowInstance(models.Model):
    workflow = models.ForeignKey(WorkflowDefinition, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='running')
    params = models.JSONField()

class TaskInstance(models.Model):
    workflow_instance = models.ForeignKey(WorkflowInstance, related_name='task_instances', on_delete=models.CASCADE)
    task = models.ForeignKey(TaskDefinition, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending')
    result = models.JSONField(null=True, blank=True)
