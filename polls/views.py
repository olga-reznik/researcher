from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db import connection
from .forms import CreateSurveyForm, DocumentForm
from django.core.files.storage import FileSystemStorage
import csv

from .models import Surveys, Questions, Choices, Questionnaires

def index(request):
    template_name = 'polls/index.html'
    context = {}

    return render(request, template_name, context)

class EditSurveyListView(generic.ListView):
    template_name = 'polls/edit_survey_list.html'
    context_object_name = 'survey_list'

    def get_queryset(self):
        return Surveys.objects.all()

class StartSurveyListView(generic.ListView):
    template_name = 'polls/start_survey_list.html'
    context_object_name = 'survey_list'

    def get_queryset(self):
        return Surveys.objects.all()

class ResultSurveyListView(generic.ListView):
    template_name = 'polls/result_survey_list.html'
    context_object_name = 'survey_list'

    def get_queryset(self):
        return Surveys.objects.all()

def survey_edit(request, survey_id):
    survey = Surveys.objects.get(pk=survey_id)

    context = {
        'survey': survey
    }

    return render(request, 'polls/survey_edit.html', context)



def survey_new(request):
    context ={}
    form = CreateSurveyForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    context['form'] = form

    return render(request, "polls/survey_new.html", context)


class SurveyQuestionsListView(generic.ListView):
    template_name = 'polls/questions_list.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Questions.objects.order_by('-pub_date')





class SurveyQuestionsListView(generic.ListView):
    template_name = 'polls/questions_list.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Questions.objects.order_by('-pub_date')


def questionnaires_list(request, survey_id):
    questionnaires_list = Questionnaires.objects.filter(survey_id=survey_id)

    context = {
        'questionnaires_list': questionnaires_list
    }
    return render(request, 'polls/questionnaires_list.html', context)


def survey_start(request, survey_id):
    survey = Surveys.objects.get(pk=survey_id)

    #При начале опроса создаем анкету
    # TODO: назначить анкете статус "Опрос начат"
    questionnaire = Questionnaires(create_date=timezone.now(), survey_id=survey_id)
    questionnaire.save()

    context = {
        'questionnaire': questionnaire,
        'survey': survey
    }

    return render(request, 'polls/start.html', context)


def vote(request):

    questionnaire = Questionnaires.objects.get(pk=request.POST['questionnaire'])
    survey = Surveys.objects.get(pk=request.POST['survey'])
    # TODO: сделать проверку анкеты. Анкета должна быть в нужном статусе, свежая, и от текущего пользователя


    status = request.POST['status']
    if status == "start":
        #Находим первый вопрос и отображаем
        first_question = Questions.objects.filter(survey_id=survey.id).order_by('sort_order').first()
        q_choices = Choices.objects.filter(question=first_question.id).order_by('sort_order')

        context = {
            'question': first_question,
            'q_choices': q_choices,
            'questionnaire': questionnaire,
            'survey': survey
        }
        return render(request, 'polls/question.html', context)
    else:
        question = Questions.objects.get(pk=request.POST['question'])

        # Сохраняем данные в анкету и переходим к следующему вопросу
        selected_choice = question.choices_set.get(pk=request.POST['choice'])

        # Название поля в анкете заранее неизвестно, вычисляем динамически
        q_index = question.q_index
        setattr(questionnaire, 'q' + str(q_index), selected_choice.choice_key )

        questionnaire.save()
        next_question = Questions.objects.filter(survey_id=survey.id, q_index__gt=question.q_index).order_by('sort_order').first()


        if next_question:
            #есть вопросы, отображаем
            q_choices = Choices.objects.filter(question=next_question.id).order_by('sort_order')

            context = {
                'question': next_question,
                'q_choices': q_choices,
                'questionnaire': questionnaire,
                'survey': survey
            }
            return render(request, 'polls/question.html', context)
        else:
            #вопросов больше нет
            # TODO: перевести анкету в статус "Опрос пройден"
            context = {
                'survey': survey
            }
            return render(request, 'polls/end.html', context)


def survey_result(request, survey_id):
    import re

    survey = Surveys.objects.get(pk=survey_id)
    question_list = Questions.objects.filter(survey_id=survey.id).order_by('sort_order')

    use_filters = False
    filters_query_str = ""
    filters_values = {}

    if request.method == 'POST':
        d1_key = request.POST.get('d1')
        d2_key = request.POST.get('d2')

        view_type = request.POST.get('view_type')
        data_type = request.POST.get('data_type')


        # Filters
        for post_key, post_value in request.POST.items():
            # Фильтр со значением =  total то же самое, что не использование фильтра
            if post_value != 'total':
                #Проверяем, что этот параметр - фильтр
                r_res = re.findall(r'filter_q_(\d*)', post_key)
                if r_res:
                    #Нашли фильтр
                    q_number = r_res[0]

                    values = request.POST.getlist(post_key)
                    filters_values[q_number] = values


        for q_number in filters_values:
            filters_query_str += """ and q"""+str(q_number)+""" in (""" + ','.join("'"+e+"'" for e in filters_values[q_number]) + """) """



    else:
        #Разрезы по умолчанию
        d1_key = str(1)
        d2_key = str(2)
        view_type = 'line'
        data_type = 'number'


    h_axis_question = Questions.objects.filter( survey_id=survey.id, q_index=d1_key ).first()
    h_axis_question_choices = Choices.objects.filter( question_id=h_axis_question.id )

    v_axis_question = Questions.objects.filter(survey_id=survey.id, q_index=d2_key).first()
    v_axis_question_choices = Choices.objects.filter(question_id=v_axis_question.id)




    query_number = """
    select q"""+d1_key+""", q"""+d2_key+""", count(id) number  from polls_questionnaires
    where survey_id="""+str(survey_id)+"""
    and q"""+d1_key+""" is not null and q"""+d2_key+""" is not null """


    query_number += filters_query_str

    query_number += """ group by  q"""+d1_key+""", q"""+d2_key+""" 
                 """

    query_percent = """
        
select t_number.q"""+d1_key+""", t_number.q"""+d2_key+""", 100*t_number.number/t_base.base percent, t_base.base, t_number.number 

 from (
select count(id) number,
       q"""+d1_key+""",
       q"""+d2_key+"""
  from polls_questionnaires
 where survey_id="""+str(survey_id)+"""
   and q"""+d1_key+""" is not null
   and q"""+d2_key+""" is not null """


    query_percent += filters_query_str

    query_percent += """ group by q"""+d1_key+""",
       q"""+d2_key+"""
) t_number

LEFT JOIN 
(
select base, q"""+d1_key+""" from (
select count(id) base,
       q"""+d1_key+"""
  from polls_questionnaires
 where survey_id=1
   and q"""+d1_key+""" is not null
   and q"""+d2_key+""" is not null """

    query_percent += filters_query_str

    query_percent += """group by q"""+d1_key+"""
 ) ) t_base
 
ON t_base.q"""+d1_key+""" = t_number.q"""+d1_key+""" """

    if data_type == 'percent':
        query = query_percent
    elif data_type == 'number':
        query = query_number
    else:
        query = query_number


    with connection.cursor() as cursor:
        cursor.execute(query)
        res = cursor.fetchall()
        results = [list(i) for i in res]


    h_axis_labels = []
    h_axis_keys_all = []
    for choice in h_axis_question_choices:
        h_axis_labels.append('q'+str(h_axis_question.q_index)+' '+h_axis_question.question_text+' c_'+choice.choice_key+' - '+choice.choice_text+' ')
        h_axis_keys_all.append(choice.choice_key)


    v_axis_labels = []
    v_axis_keys_all = []
    for choice in v_axis_question_choices:
        v_axis_labels.append( 'q'+str(v_axis_question.q_index)+' '+v_axis_question.question_text+' c_'+choice.choice_key+' - '+choice.choice_text )
        v_axis_keys_all.append(choice.choice_key)

    #Преобразуем данные из таблицы в массив

    n = len(v_axis_keys_all)
    m = len(h_axis_keys_all)
    Data = [[0] * m for i in range(n)]

    for v_index, v_key in enumerate(v_axis_keys_all, start=0):
        for h_index, h_key in enumerate(h_axis_keys_all, start=0):
            for res in results:
                if h_key == str(res[0]) and v_key == str(res[1]):
                    Data[v_index][h_index] = res[2]




    context = {
        'survey': survey,
        'results': results,
        'question_list': question_list,
        'h_axis_labels': h_axis_labels,
        'v_axis_labels': v_axis_labels,
        'h_axis_keys_all': h_axis_keys_all,
        'v_axis_keys_all': v_axis_keys_all,
        'd1_key': d1_key,
        'd2_key': d2_key,
        'Data': Data,
        'filters_values': filters_values,
        'view_type': view_type,
        'data_type': data_type

    }

    return render(request, 'polls/survey_results.html', context)

def upload_files(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        error_message = ""
        wrong_survey_ids = set([])
        wrong_question_ids = set([])

        if form.is_valid():
            doc = form.save()
            file = doc.document
            file.open(mode='r')
            reader = csv.reader(file, delimiter=';')
            iter = 0

            if doc.model_type == 'quest':
                for row in reader:
                    iter += 1
                    if iter == 1:
                        if row[0] != 'survey_id':
                            error_message += "First column must be survey_id"
                        if row[1] != 'question_test':
                            error_message += "Second column must be question_test"
                        if row[2] != 'q_index':
                            error_message += "Third column must be q_index"
                        if row[3] != 'sort_order':
                            error_message += "Fourth column must be sort_order"
                        if  error_message != "":
                            break
                    else:
                        try:
                            survey = Surveys.objects.get(id=int(row[0]))
                        except DoesNotExist:
                            wrong_survey_ids.add(row[0])
                            continue

                        question = Questions.objects.create(
                            survey=survey,
                            question_text=row[1],
                            q_index=row[2],
                            sort_order=int(row[3]),
                        )



            elif doc.model_type == 'choi':
                for row in reader:
                    iter += 1
                    if iter == 1:
                        if row[0] != 'question_id':
                            error_message += "First column must be question_id"
                        if row[1] != 'choice_text':
                            error_message += "Second column must be choice_text"
                        if row[2] != 'choice_key':
                            error_message += "Third column must be choice_key"
                        if row[3] != 'sort_order':
                            error_message += "Fourth column must be sort_order"
                        if  error_message != "":
                            break
                    else:
                        try:
                            question = Questions.objects.get(id=int(row[0]))
                        except DoesNotExist:
                            wrong_question_ids.add(row[0])
                            continue

                        choice = Choices.objects.create(
                            question=question,
                            choice_text=row[1],
                            choice_key=row[2],
                            sort_order=int(row[3]),
                        )




            form = DocumentForm()
            if len(wrong_survey_ids) != 0 :
                error_message = "Surveys with ids " + wrong_survey_ids + " do not exist. "
            if len(wrong_question_ids) != 0 :
                error_message = "Quesions with ids " + wrong_question_ids + " do not exist. "
            return render(request, 'polls/upload_files.html', {
                'form': form,
                'error_message': error_message,
            })
    else:
        form = DocumentForm()
    return render(request, 'polls/upload_files.html', {
        'form': form
    })

