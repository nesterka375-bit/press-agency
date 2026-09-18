from django.contrib.auth.models import AbstractUser
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}. Years of Experience: {self.years_of_experience}"


class Newspaper(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField()
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="newspapers"
    )
    publishers = models.ManyToManyField(Redactor, blank=True, related_name="newspapers")

    def __str__(self):
        return f"{self.name}. Topic: {self.topic.name}. Date: {self.published_date}"
