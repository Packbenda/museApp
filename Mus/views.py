from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Question, Choice,Login

def index(request):
    questions = Question.objects.all()
    return render(request, 'index.html', {'questions' : questions})


def vote(request, pk):
    question = Question.objects.get(id=pk)
    options = question.choices.all()
    return render(request, 'vote.html', {'question': question, 'options':options})

def result(request,pk):
    question = Question.objects.get(id=pk)
    options = question.choices.all()
    if request.method == 'POST':
       inputvalue = request.POST['choice']
       selection_option = options.get(id=inputvalue)
       selection_option.vote += 5
       selection_option.save()
    return render(request, 'result.html', {'question': question, 'options':options})


   
def spotify(request,pk):
  form = Login()
  if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            rep = request.POST
            rep1 = rep["song1"]
            print(rep1)
            return render(request, 'salle.html', {'form': form})
        else:
            form = Login()

  return render(request, 'spotify.html', {'form': form})















   



