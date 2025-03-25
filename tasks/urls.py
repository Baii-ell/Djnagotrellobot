from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CardViewSet, TaskViewSet, TaskDeleteView, CardDeleteView




router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'cards', CardViewSet, basename='card')
router.register(r'tasks', TaskViewSet, basename='task')



urlpatterns = [
    path('', include(router.urls)),
    path('tasks/card/<int:card_id>/', TaskViewSet.as_view({'get': 'list'}), name='task-list-by-card'),
    path('tasks/<int:task_id>/', TaskViewSet.as_view({'patch': 'update'}), name='task-update'),
    path('tasks/delete/<int:task_id>/', TaskDeleteView.as_view(), name='task-delete'),
    path('cards/delete/<int:card_id>/', CardDeleteView.as_view(), name='card-delete'),
    path('tasks/toggle/<int:pk>/', TaskViewSet.as_view({'patch': 'toggle_done'}), name='task-toggle-done'),
    path('tasks/update/<int:pk>/', TaskViewSet.as_view({'patch': 'update_task'}), name='task-update'),
]