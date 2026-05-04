from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Enrollment


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['content', 'course', 'grade']


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


class LessonAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['title', 'order', 'course']


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ['name', 'pub_date']
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Enrollment)
