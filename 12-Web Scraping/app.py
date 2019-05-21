# Import Dependencies 
from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars
import os


# Hidden authetication file
#import config 

# Create an instance of Flask app
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)



# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 

    # Find data
    mars_info = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run the scrape function
    data = scrape_mars.scrape()

    print(data)

    mongo.db.mars_info.update({}, data, upsert=True)


    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)