from django.contrib import admin
from .models import Category, Question, Choice, Quiz, QuestionResponse

class ChoiceInline(admin.TabularInline):
    model = Choice

class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']
    inlines = [ChoiceInline]
    list_display = ['__str__', 'category', 'active']
    list_editable = ['active']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Category)
# admin.site.register(Quiz)
# admin.site.register(Choice)
# admin.site.register(QuestionResponse)