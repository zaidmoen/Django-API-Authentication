from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import MeView, RegisterView, TaskViewSet

router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="task")
urlpatterns = [path("auth/register/", RegisterView.as_view()), path("auth/me/", MeView.as_view()), path("", include(router.urls))]

