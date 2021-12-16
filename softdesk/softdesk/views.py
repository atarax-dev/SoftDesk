from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response


from softapp.serializers import ProjectSerializer
from softapp.models import Project

from rest_framework import generics

from user.models import User
from user.serializers import RegisterSerializer

from softapp.serializers import ContributorSerializer

from softapp.models import Contributor

from softapp.models import Issue
from softapp.serializers import IssueSerializer

from softapp.models import Comment
from softapp.serializers import CommentSerializer


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
        queryset = self.get_queryset()
        queryset2 = queryset.filter(author=request.user)
        serializer = ProjectSerializer(none_qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            next_id_created = Project.objects.last().id
            contributor_data = {'permissions': 'a', 'role': 'createur',
                                'user': request.user.id, 'project': next_id_created}
            print("contributor data: ", contributor_data)
            contributor = ContributorSerializer(data=contributor_data)
            if contributor.is_valid():
                contributor.save(user=request.user)
                return Response(serializer.data)
            print(contributor)
            return Response(contributor.errors)

        return Response(serializer.errors)


class ProjectRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()

    def get_object(self):
        lookup_field = self.kwargs["id"]
        return get_object_or_404(Project, id=lookup_field)


class AddUserToProjectView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()

    def get(self, request, *args, **kwargs):
        lookup_field = self.kwargs["id"]
        queryset = self.get_queryset().filter(project_id=lookup_field)
        serializer = ContributorSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        lookup_field = self.kwargs["id"]
        serializer = ContributorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(project_id=lookup_field)
            return Response(serializer.data)
        return Response(serializer.errors)


class DeleteUserFromProjectView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()

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
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lookup_field = self.kwargs["id"]
        queryset = self.get_queryset().filter(project_id=lookup_field)
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        lookup_field = self.kwargs["id"]
        serializer = IssueSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(project_id=lookup_field)
            return Response(serializer.data)
        return Response(serializer.errors)


class IssueRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    queryset = Issue.objects.all()

    def get_object(self):
        lookup_field = self.kwargs["id"]
        lookup_field2 = self.kwargs["issue_id"]

        try:
            return Issue.objects.get(project_id=lookup_field, id=lookup_field2)
        except Issue.DoesNotExist:
            raise Http404


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lookup_field = self.kwargs["issue_id"]
        queryset = self.get_queryset().filter(issue_id=lookup_field)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        lookup_field = self.kwargs["issue_id"]
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(issue_id=lookup_field)
            return Response(serializer.data)
        return Response(serializer.errors)


class CommentRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def get_object(self):

        lookup_field = self.kwargs["comment_id"]
        try:
            return Comment.objects.get(id=lookup_field)
        except Comment.DoesNotExist:
            raise Http404
