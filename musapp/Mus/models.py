
from django.db import models
from django import forms

# Create your models here.
class Question(models.Model):
    
    question = models.CharField(max_length=300)

    def __str__(self):
        return self.question

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    option = models.CharField(max_length=100)
    vote = models.IntegerField(default=0)

    def __str__(self):
        return self.option

class Login(forms.Form):
     username = forms.EmailField()
     password = forms.CharField()


class ChoiceList(forms.Form):
    CHOICES = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
    ]
    like = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES, 
    )