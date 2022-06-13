from rest_framework import serializers

from .models import Course, Comment, LessonHistory, Lesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class LessonHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonHistory
        fields = "__all__"


class LessonHistoryOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonHistory
        exclude = ["student"]
