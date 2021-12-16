"""softdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from .views import ProjectListCreateView, RegisterView, ProjectRUDView, \
    AddUserToProjectView, DeleteUserFromProjectView, IssueListCreateView, IssueRUDView, CommentListCreateView, \
    CommentRUDView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('projects/', ProjectListCreateView.as_view(), name='project_list_create'),
    path('projects/<int:id>/', ProjectRUDView.as_view(), name='project_RUD'),
    path('projects/<int:id>/users/', AddUserToProjectView.as_view(), name='contributor_project'),
    path('projects/<int:id>/users/<int:user>/', DeleteUserFromProjectView.as_view(), name='delete_contributor_project'),
    path('projects/<int:id>/issues/', IssueListCreateView.as_view(), name='issue_list_create'),
    path('projects/<int:id>/issues/<int:issue_id>/', IssueRUDView.as_view(), name='issue_RUD'),
    path('projects/<int:id>/issues/<int:issue_id>/comments/',
         CommentListCreateView.as_view(), name='issue_list_create'),
    path('projects/<int:id>/issues/<int:issue_id>/comments/<int:comment_id>/',
         CommentRUDView.as_view(), name='comment_RUD'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
