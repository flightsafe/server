from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from plane import models as plane


class Course(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    cover = models.ImageField(blank=True, null=True)


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField()


class LessonHistory(models.Model):
    plane = models.ForeignKey(plane.Plane, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.FloatField(help_text=_("grade for this lesson history."), null=True, blank=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    lesson_history = models.ForeignKey(LessonHistory, on_delete=models.CASCADE, related_name="comments")
