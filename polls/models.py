import datetime 
from django.contrib.admin.decorators import display
from django.db import models
from django.utils import timezone
from django.contrib import admin 

class Question(models.Model):    
    question_text = models.CharField('Questão',max_length=200)
    pub_date = models.DateTimeField('Data Publicada')
    nivel = (
        ('F','Fácil'),
        ('M','Médio'),
        ('D','Difícil'),
        ('E','Expert'),
    )
    dificuldade = models.CharField(max_length=1, choices=nivel, default='F')
     
    @admin.display(
        boolean=True,
        ordering=['pub_date'],
        description='Publicada recentemente?', 
        )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
 
    def __str__(self) :
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) :
        return self.choice_text