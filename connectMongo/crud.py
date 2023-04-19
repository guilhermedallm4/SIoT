import pymongo
import connect_mongodb as connect
import sys 

host = 'locahost'
port = 27017
documment = 'teste'

db = connect.connectMongo(host, documment)

def crudMongoDB(option, collection, dictionary_mongo, oneValue=True, newValue={}):
    collection = db[collection]
    match option:
        case 'insert':
            if(oneValue):
                result = collection.insert_many(dictionary_mongo)
                print(result)
            else:
                result = collection.insert_one(dictionary_mongo)
                print(result)
        case 'find':
            if(oneValue):
                result = collection.find_one(dictionary_mongo)
                print(result)
            else:
                result = collection.find_many(dictionary_mongo)
                print(result)
        case 'delete':
            if(oneValue):
                result = collection.delete_one(dictionary_mongo)
                print(result)
            else:
                result = collection.delete_many(dictionary_mongo)
                print(result)
        case 'update':
            if(oneValue):
                result = collection.update_one(dictionary_mongo, newValue)
                print(result.modified_count)
            else:
                result = collection.update_many(dictionary_mongo, newValue)
                print(result.modified_count)
        case other:
                print("Please type a valid option.")
        
