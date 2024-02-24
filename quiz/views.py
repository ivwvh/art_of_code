from django.shortcuts import render
from .form import AnswerForm
# Create your views here.


questions = [
    {
        'number': 1,
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'answer_1': 'First answer',
        'answer_2': 'Second answer',
        'answer_3': 'Third answer',
    },
    {
        'number': 2,
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'answer_1': 'First answer',
        'answer_2': 'Second answer',
        'answer_3': 'Third answer',
        }
]

def index(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
    else:
        form = AnswerForm()
    context = {
        'questions': questions,
        'form': form
    }
    return render(request, 'quiz/index.html', context=context)


def about(request):
    return render(request, 'quiz/about.html')