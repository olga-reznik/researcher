from django.db import models

class Surveys(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.name

class Questions(models.Model):
    survey = models.ForeignKey(Surveys, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    q_index = models.IntegerField()
    sort_order = models.IntegerField()

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choices(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    choice_key = models.CharField(max_length=20)
    sort_order = models.IntegerField()

    def __str__(self):
        return self.choice_text


class Questionnaires(models.Model):
    survey = models.ForeignKey(Surveys, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    q1 = models.CharField(null=True, max_length=200)
    q2 = models.CharField(null=True, max_length=200)
    q3 = models.CharField(null=True, max_length=200)
    q4 = models.CharField(null=True, max_length=200)
    q5 = models.CharField(null=True, max_length=200)
    q6 = models.CharField(null=True, max_length=200)
    q7 = models.CharField(null=True, max_length=200)
    q8 = models.CharField(null=True, max_length=200)
    q9 = models.CharField(null=True, max_length=200)
    q10 = models.CharField(null=True, max_length=200)
    q11 = models.CharField(null=True, max_length=200)
    q12 = models.CharField(null=True, max_length=200)
    q13 = models.CharField(null=True, max_length=200)
    q14 = models.CharField(null=True, max_length=200)
    q15 = models.CharField(null=True, max_length=200)
    q16 = models.CharField(null=True, max_length=200)
    q17 = models.CharField(null=True, max_length=200)
    q18 = models.CharField(null=True, max_length=200)
    q19 = models.CharField(null=True, max_length=200)
    q20 = models.CharField(null=True, max_length=200)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Questionnaires._meta.fields]