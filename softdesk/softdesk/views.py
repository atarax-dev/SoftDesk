from django.db import IntegrityError
from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from softapp.serializers import ProjectSerializer
from softapp.models import Project

from rest_framework import generics, permissions, status

from user.models import User
from user.serializers import RegisterSerializer

from softapp.serializers import ContributorSerializer

from softapp.models import Contributor

from softapp.models import Issue
from softapp.serializers import IssueSerializer

from softapp.models import Comment
from softapp.serializers import CommentSerializer


class IsContribPermission(permissions.BasePermission):
    message = "Vous n'êtes pas contributeur de ce projet"

    def has_permission(self, request, view):
        project_id = view.get_project().id
        contributors = Contributor.objects.filter(project_id=project_id)
        is_contrib = contributors.filter(user=request.user).exists()
        return is_contrib


class IsOwnerOrReadOnlyPermission(permissions.BasePermission):
    message = "Vous n'êtes pas l'auteur de ce contenu"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return view.get_object().author == request.user


class IsProjectOwnerPermission(permissions.BasePermission):
    message = "Vous n'êtes pas le créateur de ce projet"

    def has_permission(self, request, view):
        return view.get_project().author == request.user


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        contributed_projects = Contributor.objects.filter(user=request.user)
        none_qs = Project.objects.none()
        for contribution in contributed_projects:
            tmp_queryset = Project.objects.filter(id=contribution.project_id)
            none_qs = none_qs | tmp_queryset
        serializer = ProjectSerializer(none_qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            next_id_created = Project.objects.last().id
            contributor_data = {'permissions': 'Créateur', 'role': 'Responsable',
                                'user': request.user.id, 'project_id': next_id_created}
            contributor = ContributorSerializer(data=contributor_data)
            if contributor.is_valid():
                contributor.save(user=request.user, project_id=next_id_created)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(contributor.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyPermission, IsContribPermission]
    queryset = Project.objects.all()

    def get_project(self):
        lookup_field = self.kwargs["id"]
        return get_object_or_404(Project, id=lookup_field)

    def get_object(self):
        lookup_field = self.kwargs["id"]
        return get_object_or_404(Project, id=lookup_field)


class AddUserToProjectView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsContribPermission, IsOwnerOrReadOnlyPermission)
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()

    def get_object(self):
        lookup_field = self.kwargs["id"]
        return get_object_or_404(Project, id=lookup_field)

    def get_project(self):
        lookup_field = self.kwargs["id"]
        return get_object_or_404(Project, id=lookup_field)

    def get(self, request, *args, **kwargs):
        lookup_field = self.kwargs["id"]
        queryset = self.queryset.filter(project_id=lookup_field)
        serializer = ContributorSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # project = self.get_object()
        # if project.author == request.user:
        try:
            lookup_field = self.kwargs["id"]
            serializer = ContributorSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(project_id=lookup_field)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Ce contributeur existe déjà")
        # else:
        # return Response(status=status.HTTP_403_FORBIDDEN, data="Vous n'êtes pas le créateur de ce contenu!" )


class DeleteUserFromProjectView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsProjectOwnerPermission)
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()

    def get_project(self):
        lookup_field = self.kwargs["id"]
        return get_object_or_404(Project, id=lookup_field)

    def get_object(self):
        lookup_field = self.kwargs["id"]
        lookup_field2 = self.kwargs["user"]

        try:
            return Contributor.objects.get(user=lookup_field2, project_id=lookup_field)
        except Contributor.DoesNotExist:
            raise Http404


class IssueListCreateView(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContribPermission]

    def get_project(self):
        lookup_field = self.kwargs["id"]
        return get_object_or_404(Project, id=lookup_field)

    def get(self, request, *args, **kwargs):
        lookup_field = self.kwargs["id"]
        queryset = self.get_queryset().filter(project_id=lookup_field)
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        lookup_field = self.kwargs["id"]
        serializer = IssueSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(project_id=lookup_field, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyPermission, IsContribPermission]
    queryset = Issue.objects.all()

    def get_project(self):
        lookup_field = self.kwargs["id"]
        return get_object_or_404(Project, id=lookup_field)

    def get_object(self):
        lookup_field = self.kwargs["id"]
        lookup_field2 = self.kwargs["issue_id"]

        try:
            return Issue.objects.get(project_id=lookup_field, id=lookup_field2)
        except Issue.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        lookup_field = self.kwargs["id"]
        serializer = IssueSerializer(data=request.data)

        if serializer.is_valid():
            serializer.data['project_id'] = lookup_field
            serializer.data['author'] = request.user
            return self.update(serializer)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsContribPermission]

    def get_project(self):
        lookup_field = self.kwargs["id"]
        return get_object_or_404(Project, id=lookup_field)

    def get(self, request, *args, **kwargs):
        lookup_field = self.kwargs["issue_id"]
        queryset = self.get_queryset().filter(issue_id=lookup_field)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        lookup_field = self.kwargs["issue_id"]
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(issue_id=lookup_field, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyPermission, IsContribPermission]
    queryset = Comment.objects.all()

    def get_project(self):
        lookup_field = self.kwargs["id"]
        return get_object_or_404(Project, id=lookup_field)

    def get_object(self):

        lookup_field = self.kwargs["comment_id"]
        try:
            return Comment.objects.get(id=lookup_field)
        except Comment.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        lookup_field = self.kwargs["issue_id"]
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.data['issue_id'] = lookup_field
            serializer.data['author'] = request.user
            return self.update(serializer)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)
