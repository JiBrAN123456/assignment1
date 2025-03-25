from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewset, UserViewset


router = DefaultRouter()
router.register(r"users", UserViewset)
router.register(r"tasks", TaskViewset, basename="task")

urlpatterns = [
    path("", include(router.urls)),

]
