from flask import *
import jwt
import ast
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling
from decouple import config

Api_booking = Blueprint('Api_booking', __name__)
key = os.getenv("JWT")

load_dotenv()
cnxpool=pooling.MySQLConnectionPool(pool_name="mypool",
                                    pool_size=10,
                                    host=os.getenv("host"),
                                    password=os.getenv("password"),
                                    user=os.getenv("user"),
                                    database=os.getenv("database"),
                                    pool_reset_session=True
                                             )

@Api_booking.route("/booking",methods=["POST"])
def booking():
    try:
        booking_info=request.json
        JWT_cookie = request.cookies.get("JWT")  
        date=booking_info['date']
        time=booking_info['time']
        fee=booking_info['fee']
        AttractionID=booking_info['AttractionID']
        if JWT_cookie: 
            cnx=cnxpool.get_connection()
            mycursor=cnx.cursor()   
            getuser=jwt.decode(JWT_cookie, key, algorithms="HS256")           
            email=getuser['email']  
            sql="SELECT email FROM booking WHERE email = %s"
            val=(email,)
            mycursor.execute(sql,val)
            records=mycursor.fetchone()
            if records == None :
                sql= "INSERT INTO booking (date , time , price , email ,AttractionID) VALUES (%s,%s,%s,%s,%s)"
                val=(date,time,fee,email,AttractionID,)
                mycursor.execute(sql,val)
                cnx.commit()
                data={
                "ok": True
                }
                return jsonify(data),200
            else:
                sql= "UPDATE booking SET date =%s , time=%s , price =%s ,AttractionID=%s where email = %s"
                val=(date,time,fee,AttractionID, email,)
                mycursor.execute(sql,val)
                cnx.commit()
                data={
                "ok": True
                }
                return jsonify(data),200

        else:
            data = {
            "error": True,
            "message": "未登入系統，拒絕存取"
            }
            return jsonify(data),403
    except:
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(data), 500
    finally:
        mycursor.close() 
        cnx.close()   


@Api_booking.route("/booking",methods=["GET"])
def get_booking():
    try:
        JWT_cookie = request.cookies.get("JWT")
        if JWT_cookie: 
            cnx=cnxpool.get_connection()
            mycursor=cnx.cursor()   
            getuser=jwt.decode(JWT_cookie, key, algorithms="HS256")
            email=getuser['email']
            sql="SELECT date,time,price,email,AttractionID FROM booking WHERE email = %s"
            val=(email,)
            mycursor.execute(sql,val)
            records=mycursor.fetchone()
            if records == None :
                data={
                    "data":None
                    }
                return jsonify(data)
            else:
                AttractionID = records[4]
                date=records[0]
                price=records[2]
                time=records[1]
                sql="SELECT name,address,images FROM attraction WHERE id = %s"
                val=(AttractionID,)
                mycursor.execute(sql,val)
                records=mycursor.fetchone()
                str=records[2]
                output=ast.literal_eval(str)
                booking_information={
                    "attraction":{
                        "id":AttractionID,
                        "name":records[0],
                        "address":records[1],
                        "image":output[0],
                    },
                    "date":date,
                    "time":time,
                    "price":price
                }              
                data={
                    "data":booking_information
                    }
                return jsonify(data),200
    except:
        data={
        "error": True,
        "message": "未登入系統，拒絕存取"
        }
        return jsonify(data),403

    finally:
        mycursor.close() 
        cnx.close()   

    
@Api_booking.route("/booking", methods=["DELETE"])
def delete_booking():
    try:
        JWT_cookie=request.cookies.get("JWT") 
        if JWT_cookie: 
            getuser=jwt.decode(JWT_cookie, key, algorithms="HS256")
            email=getuser['email']
            cnx=cnxpool.get_connection()
            mycursor=cnx.cursor()
            sql="DELETE FROM booking WHERE email=%s"
            val=(email,)
            mycursor.execute(sql,val)
            cnx.commit()
            data={
                "ok": True
                }
            return jsonify(data), 200
        else:
            data={
                "error": True, "message": "未登入系統，拒絕存取"
                }
            return jsonify(data), 403
    finally:
        mycursor.close() 
        cnx.close()  