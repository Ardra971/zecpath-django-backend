"""
URL configuration for zecpath_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from core.views import (
    JobListAPI,
    JobCreateAPI,
    UserTestAPI,
    JobDeleteAPI,
    UserRegistrationAPI,
    ApplicationCreateAPI,

    CandidateProfileAPI,
    EmployerProfileAPI,
    AdminProfileListAPI,
)


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/jobs/", JobListAPI.as_view()),
    path("api/jobs/create/", JobCreateAPI.as_view()),
    path("api/users/", UserTestAPI.as_view()),
    path("api/jobs/<int:pk>/", JobDeleteAPI.as_view()),
    path("api/register/", UserRegistrationAPI.as_view()),
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/signup/", UserRegistrationAPI.as_view(), name="signup"),
    path("api/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("api/applications/create/", ApplicationCreateAPI.as_view()),
    path("api/candidate/profile/", CandidateProfileAPI.as_view()),
    path("api/employer/profile/", EmployerProfileAPI.as_view()),
    path("api/admin/profiles/", AdminProfileListAPI.as_view()),
]