from flask import Flask, jsonify, render_template
from pymongo import MongoClient
import dbDetails
import logging
import random
from bson.json_util import dumps,loads

app = Flask(__name__)
client = ""
db = ""
collection = ""
parsedFact = {}

def connect_db():
    global client
    global db
    global collection
    try:
        client = MongoClient(dbDetails.connectionString)
        db = client[dbDetails.dbName]
        collection = db[dbDetails.colName]
    except Exception as err:
        logging.basicConfig(filename='friendsFacts.log',level=logging.ERROR)
        logging.error(err)


@app.route("/<id>")
def fetch_by_id(id):
    try:
        global client
        global db
        global collection
        global parsedFact
        connect_db()
        fact = ""
        fact = collection.find_one({"id":id},{"_id":0})
        parsedFact = {}
        parsedFact = {
            "id":fact["id"],
            "fact":fact["fact"],
        }
        if not fact["description"] =="":
            parsedFact["description"] = fact["description"]
    except Exception as err:
        logging.basicConfig(filename='friendsFacts.log',level=logging.ERROR)
        logging.error(err)
    return jsonify(dumps(parsedFact))
    


@app.route("/rnd")
def fetch_random():
    try:
        global client
        global db
        global collection
        connect_db()
        id = random.randint(2,200)
        fact = collection.find_one({"id":str(id)},{"_id":0})
        parsedFact = {}
        parsedFact = {
            "id":fact["id"],
            "fact":fact["fact"],
        }
        if not fact["description"] =="":
            parsedFact["description"] = fact["description"]
    except Exception as err:
        logging.basicConfig(filename='friendsFacts.log',level=logging.ERROR)
        logging.error(err)
    return jsonify(dumps(parsedFact))


@app.route("/list")
def fetch_all():
    try:
        global client
        global db
        global collection
        connect_db()
        facts = {}
        facts = collection.find({},{"_id":0})
    except Exception as err:
        logging.basicConfig(filename='friendsFacts.log',level=logging.ERROR)
        logging.error(err)
    return jsonify(dumps(facts))    


@app.route("/")
def landing():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
    

if __name__ == '__main__':
    app.run(port=1234,debug=True)
