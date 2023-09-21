import requests
from django.db import models

class WorkflowDefinition(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class TaskDefinition(models.Model):
    workflow = models.ForeignKey(WorkflowDefinition, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)

class Context(models.Model):
    data = models.JSONField()
    workflow_instance = models.OneToOneField('WorkflowInstance', related_name='context', on_delete=models.CASCADE)

class WorkflowInstance(models.Model):
    workflow = models.ForeignKey(WorkflowDefinition, on_delete=models.CASCADE)
    params = models.JSONField()

    def initialize_context(self):
        Context.objects.create(workflow_instance=self, data={})

    def execute_workflow(self):
        for task in self.workflow.tasks.all():
            self.execute_http_task(task)

    def execute_http_task(self, task):
        url = task.url
        params = self.params.get('query_params', {})
        headers = self.params.get('headers', {})

        try:
            # Perform the HTTP GET request
            response = requests.get(url, params=params, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                # Update the context with the response data
                context_data = self.context.data
                context_data[task.name] = response.json()
                self.context.data = context_data
                self.context.save()
            else:
                print(f"HTTP request failed for task {task.name} with status code {response.status_code}")

        except requests.RequestException as e:
            print(f"An error occurred while executing task {task.name}: {e}")
