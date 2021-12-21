from django.conf import settings
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    type = models.CharField(max_length=12, choices=[("Back-end", "Back-end"), ("Front-end", "Front-end"),
                                                    ("iOS", "iOS"), ("Android", "Android")])
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, blank=True)
    permissions = models.CharField(max_length=12, choices=[("Créateur", "Créateur"), ("Contributeur", "Contributeur")])
    role = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ('user', 'project',)

    def __str__(self):
        return self.user


class Issue(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    tag = models.CharField(max_length=12, choices=[("BUG", "BUG"), ("AMELIORATION", "AMELIORATION"),
                                                        ("TACHE", "TACHE")])
    priority = models.CharField(max_length=7, choices=[("FAIBLE", "FAIBLE"), ("MOYENNE", "MOYENNE"),
                                                        ("ELEVEE", "ELEVEE")])
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=[("A faire", "A faire"), ("En cours", "En cours"),
                                                        ("Terminé", "Terminé")])
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    assignee = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='assignee', default=author)
    created_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.CharField(max_length=140)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
