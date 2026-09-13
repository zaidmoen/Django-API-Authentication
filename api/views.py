import logging
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .decorators import require_json
from .models import Task
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
    def get_object(self): return self.request.user

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]
    def get_queryset(self): return Task.objects.filter(owner=self.request.user)
    def perform_create(self, serializer): serializer.save(owner=self.request.user)
    @action(detail=False, methods=["get"])
    def completed(self, request):
        return Response(self.get_serializer(self.get_queryset().filter(status=Task.Status.DONE), many=True).data)

