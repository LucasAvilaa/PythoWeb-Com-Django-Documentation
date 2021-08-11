from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, response
from .models import Question

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "Você está olhando o resultado da questão %s."
    return HttpResponse( response % question_id )

def vote(request, question_id):
    return HttpResponse("Você está votando na questão %s." % question_id)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html') # * Substituido pelo comando render na linha abaixo
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)