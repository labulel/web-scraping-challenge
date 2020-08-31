from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#use flask_pymongo to set up mongo connection
app.config ["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    #Find Mars data
    Mars = mongo.db.data.find_one()
    #Return the result on home page
    return render_template("index.html", data = Mars)

@app.route("/scrape")
def scraper():
    Mars = mongo.db.data
    Mars_data = scrape_mars.scrape()
    Mars.update({}, Mars_data, upsert =  True)
    return redirect("/", code = 302)

if __name__ =="__main__":
    app.run(debug = True)
