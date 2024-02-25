from django.shortcuts import render
from .form import AnswerForm
# Create your views here.


questions = [
    {
        'number': 1,
        'content': 'Correct answer is 1',
        'correct_answer': '1'
    },
    {
        'number': 2,
        'content': 'Correst answer is 2',
        'correct_answer': '2'
    },
    {
        'number': 3,
        'content': 'Correst answer is 3',
        'correct_answer': '3'
    },
]

def index(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            answer = data['answer']
            print(answer == questions[0]['correct_answer']) 
            context = {
                'questions': questions,
                'form': form,
                'answer': answer
            }
            return render(request,
                          'quiz/index.html',
                          context=context)
    else:
        form = AnswerForm()
    context = {
        'questions': questions,
        'form': form
    }
    return render(request, 'quiz/index.html', context=context)


def about(request):
    return render(request, 'quiz/about.html')