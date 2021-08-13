from django.contrib import admin
from django.contrib.admin.filters import ListFilter 
from .models import Question,Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Nome', {'fields':['question_text']}),
        (None, {'fields':['dificuldade']}, ),
        ('Data Publicada',{'fields':['pub_date']})
    ]
    list_display = ('question_text','pub_date', 'dificuldade','was_published_recently')
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
