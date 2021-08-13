from django.contrib import admin

from .models import Surveys, Questions, Choices, Questionnaires

#admin.site.register(Surveys)
#admin.site.register(Questions)
#admin.site.register(Choices)



class ChoicesInline(admin.TabularInline):
    model = Choices
    extra = 5


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'q_index', 'sort_order' )
    list_filter = ['survey']
    search_fields = ['survey', 'question_text', 'q_index', 'sort_order']
    inlines = [ChoicesInline]

admin.site.register(Questions, QuestionsAdmin)


class QuestionsInline(admin.TabularInline):
    model = Questions
    extra = 5


class SurveysAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date')
    list_filter = ['name', 'create_date']
    search_fields = ['name', 'create_date']
    inlines = [QuestionsInline]

admin.site.register(Surveys, SurveysAdmin)




admin.site.register(Questionnaires)