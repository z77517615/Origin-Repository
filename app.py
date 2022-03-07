from flask import *
from api.api import Attraction
from mysql.connector import pooling
import mysql.connector


app=Flask(__name__)
app.register_blueprint(Attraction, url_prefix='/api')

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")
	
app.run(host='0.0.0.0', port=3000)

