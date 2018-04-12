#-*- coding:utf-8 -*-

from config import config
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from pymongo import MongoClient
from collections import deque
import requests
import string
import json
import datetime 
import random

ans = list()
res_list = list()
chat = list()
list2dict = {}

# Create your views here.

def index(request):

    global chat
    chat = list()
    list2dict["chat"] = chat
    request.session['chat'] = json.dumps(list2dict["chat"])

    return render(request, 'training.html',locals())

def training(request):

    global ans
    global res_list
    global chat
    global list2dict

    chat = json.loads(request.session['chat'])    

    url = config.CHATBOT_URL

    if 'question' not in request.POST:
       return render(request, 'training.html', {"chat" : chat})
    
    else: 

       ans.append(request.POST['question']) 
       data = {'dialog' : ans} 
       response = requests.post(url, json=data)

       res = json.loads(str(response.text))

       if "res_list" in res:
          res_list = res["res_list"] 
          print ("list")
     
          chat.append(request.POST['question'])
          if len(chat) > 8:
             chat = remove_element(chat)

          list2dict["chat"] = chat
          request.session['chat'] = json.dumps(list2dict["chat"])
          print (chat)

          return render(request, 'training.html', {'res_list0' : res_list[0], 'res_list1' : res_list[1], 'res_list2' : res_list[2], "chat" : chat})

       else:
          res_str = res["init_res_str"]
          print ("str")

          chat.append(request.POST['question'])
          if len(chat) > 8:
             chat = remove_element(chat)

          chat.append(res_str)
          if len(chat) > 8:
             chat = remove_element(chat)

          list2dict["chat"] = chat
          request.session['chat'] = json.dumps(list2dict["chat"])
          print (chat)

          creation_date = datetime.datetime.now()

          dict = {"question" : chat[-6:-1], "res_list0" : { "res_list0" : "none", "score0" : 0 }, "res_list1" : { "res_list1" : "none", "score1" : 0 }, "res_list2" : { "res_list2" : "none" , "score2" : 0 }, "suggestion" : { "suggestion" : "none", "score3" : 0 }, "creation_date" : creation_date }
  
          mongo_save(dict)
 
          return render(request, 'training.html', {"res_str" : res_str,  "chat" : chat})


def result_save(request):

    global res_list
    global chat
    chosen_list = list()

    print ("result_save")

    print (request.POST['score0'])
    score0 = request.POST['score0']

    print (request.POST['score1'])
    score1 = request.POST['score1']

    print (request.POST['score2'])
    score2 = request.POST['score2']

    print (request.POST['score3'])
    score3 = request.POST['score3']

    suggestion = (request.POST['suggestion'])
    print (request.POST['suggestion'])
    print (type(request.POST['suggestion']))

    if suggestion:

       chosen = suggestion

       chat.append(chosen)
       if len(chat) > 8:
          chat = remove_element(chat)

       list2dict["chat"] = chat
       request.session['chat'] = json.dumps(list2dict["chat"])
       print ("suggestion")
       print (chat)


    else:
       print ("suggestion=none")
       suggestion = "none"

       score = max(int(request.POST['score0']), int(request.POST['score1']), int(request.POST['score2']))

       if score == int(request.POST['score0']):
          chosen_list.append(res_list[0])

       if score == int(request.POST['score1']):
          chosen_list.append(res_list[1])

       if score == int(request.POST['score2']):
          chosen_list.append(res_list[2])

       print (chosen_list)
       print (score)

       chosen = chosen_list[random.randint(0,len(chosen_list)-1)]

       chat.append(chosen)
       if len(chat) > 8:
          chat = remove_element(chat)

       list2dict["chat"] = chat
       request.session['chat'] = json.dumps(list2dict["chat"])
       print ("no suggestion")
       print (chat)

    print (ans[0])
    print (res_list[0])
    print (res_list[1])
    print (res_list[2])

    creation_date = datetime.datetime.now()

    dict = {"question" : chat[-6:-1], "res_list0" : { "res_list0" : res_list[0], "score0" : score0 }, "res_list1" : { "res_list1" : res_list[1], "score1" : score1 }, "res_list2" : { "res_list2" : res_list[2] , "score2" : score2 }, "suggestion" : { "suggestion" : suggestion, "score3" : score3 }, "creation_date" : creation_date }
    mongo_save(dict)
    
    return render(request, 'training.html', {"chat" : chat})


def welcome(request):
    if 'user_name' in request.GET:
        return HttpResponse('Welcome!~'+request.GET['user_name'])
    else:
        return render_to_response('welcome.html',locals())


def test_session(request):

    keeps = {"john" : "chen"}
    request.session['lucky_number'] = json.dumps(keeps)               # 設置lucky_number

    if 'lucky_number' in request.session:
        lucky_number = request.session['lucky_number']                # 讀取lucky_number

        response = HttpResponse('Your lucky_number is '+lucky_number)
    del request.session['lucky_number']                               # 刪除lucky_number

    return response


def remove_element(chatlist):
  
    chatlist.reverse()
    chatlist.pop()
    chatlist.pop()
    chatlist.reverse()
   
    return chatlist

  
def mongo_save(dict):

    #client = MongoClient("mongodb://%s:%s@%s/%s" % (config.MONGODB_USERNAME, config.MONGODB_PASSWORD, config.MONGODB_DATABASE_URL, config.MONGODB_DBNAME))

    client = MongoClient("mongodb://%s/%s" % (config.MONGODB_DATABASE_URL, config.MONGODB_DBNAME))
    db = client.chatbotroom
    collection = db.training

    collection.insert_one(dict)

    return 
