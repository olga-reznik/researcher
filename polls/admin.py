from django.contrib import admin

from .models import Surveys, Questions, Choices, Questionnaires

admin.site.register(Surveys)
admin.site.register(Questions)
admin.site.register(Choices)
admin.site.register(Questionnaires)