from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Quiz, Question, CustomUser, Role


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = CustomUser 
        fields = ("username", "email", "password1", "password2", 'role')
        

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
    

class QuizForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Выбрать учеников'
    )

    class Meta:
        model = Quiz
        fields = ['title','passing_score', 'students']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        print("QuizForm request:", self.request)
        if self.request.user.is_authenticated and self.request.user.role == Role.TEACHER:
            self.fields['students'].queryset = CustomUser.objects.filter(teacher=self.request.user, role=Role.STUDENT)
        elif self.request.user.is_authenticated:
            self.fields['students'].queryset = CustomUser.objects.filter(teacher=self.request.user, role=Role.STUDENT)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['content', 'ans_1',
                  'ans_2', 'ans_3', 'correct', 'quiz']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['test'].queryset = Quiz.objects.filter(author=user)


class TeacherSelectionForm(forms.Form):
    teacher = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='T'),
        label='Select your teacher',
        empty_label='Select a teacher'
    )