from django.contrib import admin
from .models import Category, Question, Choice, Quiz, QuestionResponse

class ChoiceInline(admin.TabularInline):
    model = Choice

class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']
    inlines = [ChoiceInline]
    list_display = ['__str__', 'category', 'published']
    list_editable = ['published']
    search_fields = ['question_text']



class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']
    list_display = ['__str__', 'published']
    list_editable = ['published']
    search_fields = ['name']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(Quiz)
# admin.site.register(Choice)
# admin.site.register(QuestionResponse)