from pydoc import doc
from pymongo import MongoClient
import pymongo
from pymongo import MongoClient
import json
import os
def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # username = os.environ.get('mongoDb')
    f = open("monogDBURI.txt", "r")
    CONNECTION_STRING = f.read()
    f.close()

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['deployment']
    
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    # Get the database
    dbname = get_database()
    print(dbname.list_collection_names())
    cursor = dbname['profiles'].find()
    # with open('output.json', 'w') as outfile:
    #     for document in cursor:
    #         json.dumps(document, outfile)
    with open('output.json', 'w') as outfile:
        for document in cursor:
            # for k, v in document.items():
            #     if (k == "_id" or k == "user"):
            #         document[k] = str(v)
            #     # print(k, v)
            document["_id"] = str(document["_id"])
            document["user"] = str(document["user"])
            for item in document["expertise"]:
                item["_id"] = str(item["_id"])
            document["date"] = str(document["date"])

            json.dump(document, outfile, indent = 2)
