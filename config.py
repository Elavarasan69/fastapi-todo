
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://elavarasantamil:1234@elavarasancluster.oxh3vfs.mongodb.net/?appName=ElavarasanCluster"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.todo_db
collection = db["todo_data"]