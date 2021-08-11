from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),

    path('edit_survey/', views.EditSurveyListView.as_view(), name='edit_survey_list'),
    path('survey/<int:survey_id>/edit/', views.survey_edit, name='survey_edit'),

    path('start_survey/', views.StartSurveyListView.as_view(), name='start_survey_list'),
    path('survey/<int:survey_id>/start/', views.survey_start, name='survey_start'),

    path('result_survey/', views.ResultSurveyListView.as_view(), name='result_survey_list'),
    path('survey/<int:survey_id>/results/', views.survey_result, name='survey_result'),


    path('create_survey/', views.survey_new, name='survey_new'),

    path('questionnaires/<int:survey_id>/', views.questionnaires_list, name='questionnaires_list'),

    path('survey/<int:pk>/questions/', views.SurveyQuestionsListView.as_view(), name='survey_questions_list'),

    path('question/vote/', views.vote, name='vote'),



]