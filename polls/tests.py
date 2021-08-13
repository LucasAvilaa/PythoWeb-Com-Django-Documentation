import datetime
from django.http import response
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_futute_question(self):
        """
            was_published_recently() retorna Falso para perguntas cuja pub_date está no futuro        
        """
        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def text_was_published_recently_with_old_question(self):
        """
        was_published_recently() retorna Falso para perguntas cuja pub_date é mais de 1 dia.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def text_was_published_recently_with_recente_question(self):
        """
        was_published_recently() retorna True para perguntas cuja pub_date está dentro do último dia.
        """     
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recente_question = Question(pub_date=time)
        self.assertIs(recente_question.was_published_recently(), True)

def create_question(question_text, days):
    """ 
        Criar uma pergunta com o dado 'question_text' e publicou o dado número de 'dias' compensado até 
        agora (negativo para perguntas publicadas no passado, positivo para questões que ainda não foram 
        publicadas).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
            Se não houver perguntas, uma mensagem apropriada será exibida
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sem artigos disponíveis.')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        """
            Perguntas com um pub_date no passado são exibidas no página de índice.
        """ 
        question_past = create_question(question_text='Questão no passado', days=-30)
        response = self.client.get(reverse('polls:index')) 
        self.assertQuerysetEqual(response.context['latest_question_list'],[question_past])

    def test_future_question(self):
        """
            Perguntas com um pub_date no futuro não são exibidas em a página do índice.
        """
        create_question(question_text='Questão Futura', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'Sem artigos disponíveis.')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_future_question_and_past_question(self):
        """
        Mesmo que existam perguntas passadas e futuras, apenas perguntas passadas são exibidos. 
        """
        create_question(question_text='Questão Futura', days=30)
        past_question = create_question(question_text='Questão passada', days=-30)
        response = self.client.get(reverse('polls:index'))   
        self.assertQuerysetEqual(response.context['latest_question_list'],[past_question])

    def test_two_past_question(self):
        """
            A página de índice de perguntas pode exibir várias perguntas.
        """
        question_1 = create_question(question_text="Questão 1", days=-2)
        question_2 = create_question(question_text="Questão 2", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],[question_1,question_2])

class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """
            A visão detalhada de uma pergunta com um pub_date no futuro retorna um 404 não encontrado. 
        """
        future_question = create_question(question_text='Questão Futura',days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """ 
            A visão detalhada de uma pergunta com um pub_date no passado exibe o texto da pergunta.
        """ 
        past_question = create_question(question_text='Questão passada', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)