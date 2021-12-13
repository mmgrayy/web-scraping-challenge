xfrom flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Flask
app = Flask(__name__)


# set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html 
@app.route("/")
def index():

    # call mongo database
    mars_dict = mongo.db.mars_dict.find_one()
    # Return data
    return render_template("index.html", mars=mars_dict)


@app.route("/scrape")
def scrape():
  
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()
    # Update the Mongo database
    mars_dict.update_many({}, {"$set": mars_data}, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)