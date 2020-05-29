from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(prefix='users', viewset=UserViewSet)
router.register(prefix='products', viewset=ProductViewSet)
router.register(prefix='posts', viewset=PostViewSet)
router.register(prefix='schedules', viewset=ScheduleViewSet)
router.register(prefix='courses', viewset=CourseViewSet)
router.register(prefix='lockers', viewset=LockerViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
