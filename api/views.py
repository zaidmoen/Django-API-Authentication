import logging
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .decorators import require_json
from .models import Task
from .pagination import TaskPagination
from .permissions import IsOwner
from .serializers import RegisterSerializer, TaskSerializer

logger = logging.getLogger("api")
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @require_json
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        logger.info("New user registration attempted: status=%s", response.status_code)
        return response


class MeView(generics.RetrieveAPIView):
    serializer_class = RegisterSerializer

    def get_object(self):
        return self.request.user


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]
    pagination_class = TaskPagination

    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)
        status_value = self.request.query_params.get("status")
        priority_value = self.request.query_params.get("priority")
        category_value = self.request.query_params.get("category")
        search_value = self.request.query_params.get("search")

        if status_value:
            queryset = queryset.filter(status=status_value)
        if priority_value:
            queryset = queryset.filter(priority=priority_value)
        if category_value:
            queryset = queryset.filter(category__iexact=category_value)
        if search_value:
            queryset = queryset.filter(title__icontains=search_value)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"])
    def completed(self, request):
        completed_tasks = self.get_queryset().filter(status=Task.Status.DONE)
        return Response(self.get_serializer(completed_tasks, many=True).data)
