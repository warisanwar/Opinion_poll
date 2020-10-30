from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question_name']}),]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)