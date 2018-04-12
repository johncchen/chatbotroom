import os

#MONGODB_SETTINGS = {
#    'mongodb_host': os.environ.get('MONGODB_DATABASE_URL'),
#    'mongodb_password': os.environ.get('MONGODB_PASSWORD', None),
#    'mongodb_username': os.environ.get('MONGODB_USERNAME', None),
#    'mongodb_db': os.environ.get('MONGODB_DB', None),
#    'tz_aware': True,
#}

##MONGODB_DATABASE_URL = "13.113.25.25:27017"
MONGODB_DATABASE_URL = os.environ.get('MONGODB_DATABASE_URL')

##MONGODB_USERNAME = "charbotroom"
MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME')

##MONGODB_PASSWORD = "nuwa8888"
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')

##MONGODB_DBNAME = "chatbotroom"
MONGODB_DBNAME = os.environ.get('MONGODB_DBNAME')

##CHATBOT_URL = "http://dev-cognitive.nuwarobotics.cn:5006/v3/chatbot/"
CHATBOT_URL = os.environ.get('CHATBOT_URL')
