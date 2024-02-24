from django import forms


class AnswerForm(forms.Form):
    choices = [
        ('1', 'Answer 1'),
        ('2', 'Answer 2'),
        ('3', 'Answer 3'),
    ]
    answer = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=choices
    )
