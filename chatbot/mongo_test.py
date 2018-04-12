from pymongo import MongoClient

client = MongoClient("mongodb://chatbotroom:nuwa8888@127.0.0.1:27017/chatbotroom")

db = client.chatbotroom

collection = db.training

mydict = {"name":"john", "sex":"male","job":"devops"}

mylist = []

mylist.append(mydict)

collection.insert_many(mylist)

counts = collection.find().count()

print (counts)
