from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Quiz, Role, QuizAssignment, QuizResult
from .forms import QuestionForm, QuizForm, CustomUserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import TeacherSelectionForm


@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    return redirect('home')


@login_required
def indexview(request):
    if request.user.role == Role.STUDENT:
        quiz_assignments = QuizAssignment.objects.filter(student=request.user)
        quizes = [assignment.quiz for assignment in quiz_assignments]
    elif request.user.role == Role.TEACHER:
        quizes = Quiz.objects.filter(author=request.user)
    return render(request, 'quiz/main.html', {'quizes': quizes})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/registration.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


class QuizCreateView(CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'quiz/quiz_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        print("QuizCreateView request:", self.request)
        return kwargs
    
    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.author = self.request.user
        form.save()
        for student in form.cleaned_data['students']:
            student.assign_quiz(form.instance)
        return redirect('quiz_edit', self.object.id)


class QuizEditView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_edit.html'
    success_url = reverse_lazy("quiz_edit")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = self.object.questions.all()
        return context


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'quiz/question_form.html'
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['test'].queryset = Quiz.objects.filter(author=user) 

    def form_valid(self, form):
        self.object = form.save()
        return redirect(reverse('quiz_edit', kwargs={'pk': self.object.quiz.pk})) 
    



class TeacherSelectionView(LoginRequiredMixin, FormView):
    form_class = TeacherSelectionForm
    template_name = 'quiz/teacher.html'
    success_url = '/'

    def form_valid(self, form):
        self.request.user.teacher = form.cleaned_data['teacher']
        self.request.user.save()
        return super().form_valid(form)


class AboutView(TemplateView):
    template_name = 'quiz/about.html'


def quiz_detail(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = quiz.questions.all()
    context = {'quiz': quiz, 'questions': questions, 'quiz_id':quiz_id}
    return render(request, 'quiz/quiz_detail.html', context)

def submit_quiz(request, id):
    if request.method == 'POST':
        quiz = Quiz.objects.get(pk=id)
        questions = quiz.questions.all()
        score = 0
        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')
            if getattr(question, user_answer) == question.correct:
                score += 1
        passed = score >= quiz.passing_score
        QuizResult.objects.create(student=request.user, quiz=quiz, score=score, passed=passed)
        return render(request, 'quiz/view_results.html', {'quiz': quiz,'score': score, 'passed': passed})


class QuizStatisticsView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.object
        pass_rate, passed_students = self.calculate_pass_rate_and_passed_students(quiz)
        context['pass_rate'] = pass_rate
        context['passed_students'] = passed_students
        return context

    def calculate_pass_rate_and_passed_students(self, quiz):
        total_students = QuizAssignment.objects.filter(quiz=quiz).count()
        passed_students = QuizResult.objects.filter(quiz=quiz, passed=True)
        pass_rate = (passed_students.count() / total_students) * 100 if total_students > 0 else 0
        return pass_rate, passed_students
    

def profile_view(request):
    if request.user.is_authenticated:
        if request.user.role == Role.TEACHER:
            students = QuizAssignment.objects.filter(quiz__author=request.user).values_list('student', flat=True).distinct()
            context = {'is_teacher':True, 'students': students}
        elif request.user.role == Role.STUDENT:
            teacher = request.user.teacher
            context = {'is_student': True, 'teacher': teacher}
        return render(request, 'quiz/profile.html', context)
    else:
        return redirect('login')