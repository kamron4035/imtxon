from random import shuffle, sample

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render,redirect
from django.core.cache import cache
from django_filters.views import FilterView
from .filters import ResultFilter
from .models import Question, Result, QuizType
from .utils import check_answer

User = get_user_model()


def qiuz(request):
    quizs = QuizType.objects.all()
    context = {
        'quizs': quizs
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
def question(request, pk):
    questions = Question.objects.filter(quiz_id=pk)
    if questions.count() > 5:
        questions = sample(list(questions), 5)
    else:
        questions = sample(list(questions), questions.count())
    if request.method == "POST":
        context = check_answer(request)
        cache.delete('questions')
        return render(request, 'quizapp/result.html', context)

    if not cache.get('questions'):
        cache.set('questions', questions, timeout=360)
    questions = cache.get('questions')
    context = {
        'questions': questions,
    }
    return render(request, 'quizapp/question.html', context)


def result_list(request):
    results = Result.objects.all()
    context = {
        'results': results
    }
    return render(request, 'quizapp/result_list.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password, username)
        user = authenticate(request, username=username, password=password)
        if not user:
            messages.error(request, "User not found")
            return render(request, 'registration/login.html')
        login(request, user)
        messages.info(request, 'Login successfull!')
        return redirect('home')
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Logout successfull')
    return redirect('login')


class ResultView(FilterView):
    model = Result
    template_name = 'quizapp/result_list.html'
    context_object_name = 'results'
    filterset_class = ResultFilter

    def get_result_list(request):
        results = Result.objects.all()
        context = {
            'results': results
        }
        return context
    #
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context[''] = self.category()
    #     context['tags'] = self.tag()
    #     context['test'] = "Test xabar"
    #     return context