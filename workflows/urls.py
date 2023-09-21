from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'workflow-definitions', views.WorkflowDefinitionViewSet)
router.register(r'task-definitions', views.TaskDefinitionViewSet)
router.register(r'workflow-instances', views.WorkflowInstanceViewSet)
router.register(r'task-instances', views.TaskInstanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
