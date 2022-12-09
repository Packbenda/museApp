from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from .models import Question, Choice,Login,ChoiceList

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import getpass
import random
import re 
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import urllib3
import base64



def index(request):
    questions = Question.objects.all()
    return render(request, 'index.html', {'questions' : questions})


def vote(request, pk):
    question = Question.objects.get(id=pk)
    options = question.choices.all()

    X=pd.read_csv('playlist.csv')
    L=[X.iloc[:,0][i] for i in range (len(X))] 
    global scoreList
    scoreList = [0] * len(L)
    


    return render(request, 'vote.html', {'question': question, 'options':options, 'L':L,'nbr':[0,1,2,3,4]})


def salle(request, pk):
    question = Question.objects.get(id=pk)
    options = question.choices.all()
    return render(request, 'salle.html', {'question': question, 'options':options})

def result(request,pk):
    question = Question.objects.get(id=pk)
    options = question.choices.all()
    X=pd.read_csv('playlist.csv')
    L=[X.iloc[:,0][i] for i in range (len(X))] 
    l = [5 for i in range(len(L))]
    v = dict(zip(L, l))
    #scoreList = [0] * len(L)
    global scoreList

    if request.method == 'POST':
        ch = request.POST['choice']
        counteur = 0
        for l in L:
            if ch == l:
                scoreList[counteur] += 1
            counteur += 1
        
        ListScore = {k:v for k,v in zip(L,scoreList)}
        lst = list(v.values())

    return render(request, 'result.html', {'question': question, 'options':options,'List':ListScore,'nbr':[0,1,2,3,4],'lst':lst})


   
def spotify(request,pk):
  question = Question.objects.get(id=pk)
  form = Login()
  if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            url = "https://accounts.spotify.com/fr/login?continue=https%3A%2F%2Fopen.spotify.com%2F__noul__%3Fl2l%3D1%26nd%3D1&_locale=fr-FR"
            driver=webdriver.Chrome()
            driver.get(url)
            driver.maximize_window()

            id = driver.find_element(by=By.ID,value='login-username')
            id.send_keys(username)

            mdp = driver.find_element(by=By.ID,value='login-password')
            mdp.send_keys(password)

            login= driver.find_element(by=By.ID, value='login-button')
            login.click()

            #url = "https://accounts.spotify.com/fr/login?continue=https%3A%2F%2Fopen.spotify.com%2F__noul__%3Fl2l%3D1%26nd%3D1&_locale=fr-FR"
            url = "https://accounts.spotify.com/fr/login"
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            driver=webdriver.Chrome(executable_path="chromedriver.exe",chrome_options=options)
            
            driver.get(url)
            driver.maximize_window()
            
            id = driver.find_element(by=By.ID,value='login-username')
            id.send_keys(username)

            mdp = driver.find_element(by=By.ID,value='login-password')
            mdp.send_keys(password)

            login= driver.find_element(by=By.ID, value='login-button')
            login.click()

            time.sleep(2)
            timeout_in_seconds = 4

            #Close=driver.find_element_by_xpath("/html/body/div[15]/div/div/div/div[2]/button[2]").click() 
            Close=driver.find_element(by=By.XPATH,value='//*[@id="root"]/div/div[2]/div/div/button[2]')
            Close.click()   
            #WebDriverWait(driver, timeout_in_seconds).until(ec.element_to_be_clickable((By.XPATH, '//[@id="root"]/div/div[2]/div/div/button[2]'))).click()
            time.sleep(2)
            #WebDriverWait(driver, timeout_in_seconds).until(ec.element_to_be_clickable((By.XPATH, '//[@id="main"]/div/div[2]/nav/div[1]/ul/li[3]/div/a/span'))).click()

            Tout_Afficher = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/nav/div[1]/ul/li[3]/div/a/span').click()

            time.sleep(2)
            requesting = requests.get(url)
            time.sleep(2)
            src=driver.page_source
            time.sleep(2)
            soup= BeautifulSoup(src, "lxml") #you can't put driver.page_source directly into the BeautifulSoup
            time.sleep(2)

            Playlist_Full = soup.find('div',{"data-testid":"grid-container"})
            Playlist_Half_Full=Playlist_Full.find_all('div',{"class":"LunqxlFIupJw_Dkx6mNx"})
            Playlist = Playlist_Full.find_all('a',{"draggable":"false"})
            S=str(Playlist)
            Playlist_L = re.findall(r'title=\"([\w ]*)\"',S) #à afficher pour que l'utilisateur choisisse


            L= Playlist_L         
            M={"playlist": L}
            M=pd.DataFrame(L)
            M.to_csv("playlist.csv",index=False)

            return render(request, 'salle.html', {'question': question,'form': form, 'L':L})
        else:
            form = Login()
  return render(request, 'spotify.html', {'question': question,'form': form})


