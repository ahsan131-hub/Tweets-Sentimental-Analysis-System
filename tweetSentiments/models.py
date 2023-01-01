from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=2000)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)