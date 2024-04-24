from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
urlpatterns = [
    path("health",views.HealthRoute.as_view(),name="health_route"),
    path('register',views.Register.as_view(),name="register"),
    path('login',views.Login.as_view(),name="login"),
    path('task',views.Task.as_view(),name="task"),
    path('all-tasks',views.TaskList.as_view(),name="task_list"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify')
]