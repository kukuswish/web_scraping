from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsScrape_DB"
mongo = PyMongo(app)

# Or set inline

@app.route("/")
def index():
    info = list(mongo.db.marsInfo.find())
    ds=info[-1]

    return render_template("index.html", data=ds)


@app.route("/scrape")
def scraper():
    scrapeData = mongo.db.marsInfo
    mars_data = scrape_mars.scrapeData()


    mongo.db.marsInfo.insert_one(mars_data)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
