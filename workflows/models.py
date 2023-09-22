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
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True)


class Context(models.Model):
    data = models.JSONField()
    workflow_instance = models.OneToOneField('WorkflowInstance', related_name='context', on_delete=models.CASCADE)


class WorkflowInstance(models.Model):
    workflow = models.ForeignKey(WorkflowDefinition, on_delete=models.CASCADE)
    params = models.JSONField()

    def save(self, *args, **kwargs):
        is_new = not self.pk  # Check if this is a new instance
        super().save(*args, **kwargs)
        if is_new:
            self.initialize_context()  # Initialize the context
            self.initialize_task_instances()  # Initialize the task instances

    def initialize_task_instances(self):
        for task_definition in self.workflow.tasks.all():
            TaskInstance.objects.create(task_definition=task_definition, workflow_instance=self)

    def initialize_context(self):
        if not hasattr(self, 'context'):
            Context.objects.create(workflow_instance=self, data={})

    def execute_workflow(self):
        # Repeatedly loop through tasks until all are either 'success' or 'failed'
        while self.task_instances.filter(state='to_do').exists():
            for task_instance in self.task_instances.filter(state='to_do'):
                if task_instance.are_dependencies_met():
                    self.execute_http_task(task_instance)

    def execute_http_task(self, task_instance):
        task_instance.state = 'in_progress'
        task_instance.save()

        url = task_instance.task_definition.url
        params = self.params.get('query_params', {})
        headers = self.params.get('headers', {})

        try:
            # Perform the HTTP GET request
            response = requests.get(url, params=params, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                # Update the context with the response data
                context_data = self.context.data
                context_data[task_instance.task_definition.name] = response.json()
                self.context.data = context_data
                self.context.save()

                task_instance.state = 'success'
                task_instance.save()
            else:
                task_instance.state = 'failed'
                task_instance.save()
                print(
                    f"HTTP request failed for task {task_instance.task_definition.name} with status code {response.status_code}")

        except requests.RequestException as e:
            print(f"An error occurred while executing task {task_instance.task_definition.name}: {e}")


class TaskInstanceState(models.TextChoices):
    TO_DO = 'to_do', 'To Do'
    IN_PROGRESS = 'in_progress', 'In Progress'
    SUCCESS = 'success', 'Success'
    FAILED = 'failed', 'Failed'


class TaskInstance(models.Model):
    task_definition = models.ForeignKey(TaskDefinition, related_name='task_instances', on_delete=models.CASCADE)
    workflow_instance = models.ForeignKey(WorkflowInstance, related_name='task_instances', on_delete=models.CASCADE)
    state = models.CharField(
        max_length=12,
        choices=TaskInstanceState.choices,
        default=TaskInstanceState.TO_DO
    )

    def are_dependencies_met(self):
        dependencies = self.task_definition.dependencies.all()
        for dependency in dependencies:
            try:
                instance = TaskInstance.objects.get(task_definition=dependency,
                                                    workflow_instance=self.workflow_instance)
                if instance.state != 'success':
                    return False
            except TaskInstance.DoesNotExist:
                return False
        return True
