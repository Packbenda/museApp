
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
   song1 = forms.CharField()
   song2 = forms.CharField()
   song3 = forms.CharField()
   song4 = forms.CharField()
   song5 = forms.CharField()

   def __str__(self):
        return self.song1
   def __str__(self):
        return self.song2
   def __str__(self):
        return self.song3
   def __str__(self):
        return self.song4
   def __str__(self):
        return self.song5
 