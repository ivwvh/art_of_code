from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class Role(models.TextChoices):
    TEACHER = 'T', 'Teacher'
    STUDENT = 'S', 'Student'


class CustomUser(AbstractUser):
    role = models.CharField(max_length=1, choices=Role)
    teacher = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def assign_quiz(self, quiz):
        QuizAssignment.objects.create(quiz=quiz, student=self)

class Statistics(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='stats')

    correct_answers_total = models.IntegerField(default=0)
    wrong_answers_total = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'Stats for {self.user}'
    

class Quiz(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='quizes')
    completed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='completed')
    passing_score = models.IntegerField(verbose_name='Проходной балл', default=0)
    def get_absolute_url(self):
        return reverse("quiz_edit", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f'{self.title}' 
    
    
class Question(models.Model):
    content = models.TextField(verbose_name='Содержание')
    ans_1 = models.CharField(verbose_name='Ответ 1',max_length=100, null=True)
    ans_2 = models.CharField(verbose_name='Ответ 2', max_length=100, null=True)
    ans_3 = models.CharField(verbose_name= "Ответ 3",max_length=100, null=True)
    correct = models.CharField(verbose_name='Верный ответ',max_length=100, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, related_name='questions', verbose_name='Ответ для викторины')


class QuizAssignment(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quiz.title} - {self.student.username}'
    


class QuizResult(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Ученик')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Викторина')
    score = models.IntegerField(verbose_name='Баллов получено')
    passed = models.BooleanField(default=False, verbose_name='Пройден тест')

    def __str__(self):
        return f'{self.student.username} - {self.quiz.title}'