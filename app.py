from flask import *
from api.attraction import Attraction
from api.member import member
from api.booking import Api_booking
from mysql.connector import pooling
import mysql.connector
from decouple import config

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False
app.secret_key="123123123"  
app.register_blueprint(Attraction, url_prefix='/api')
app.register_blueprint(member, url_prefix='/api')
app.register_blueprint(Api_booking, url_prefix='/api')

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
	
app.run(host='0.0.0.0', port=3000,debug=True)

