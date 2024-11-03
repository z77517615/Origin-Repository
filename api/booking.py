from flask import Blueprint, request, jsonify
import jwt
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling

load_dotenv()

Api_booking = Blueprint('Api_booking', __name__)
key = os.getenv("JWT")

cnxpool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,
    host=os.getenv("host"),
    password=os.getenv("password"),
    user=os.getenv("user"),
    database=os.getenv("database"),
    pool_reset_session=True
)

@Api_booking.route("/booking", methods=["POST"])
def booking():
    try:
        booking_info = request.json
        JWT_cookie = request.cookies.get("JWT")
        date = booking_info['date']
        time = booking_info['time']
        fee = booking_info['fee']
        AttractionID = booking_info['AttractionID']
        
        if JWT_cookie:
            getuser = jwt.decode(JWT_cookie, key, algorithms="HS256")
            email = getuser['email']
            
            with cnxpool.get_connection() as cnx:
                with cnx.cursor() as myCursor:
                    sql = "SELECT email FROM booking WHERE email = %s"
                    val = (email,)
                    myCursor.execute(sql, val)
                    records = myCursor.fetchone()
                    
                    if records is None:
                        sql = "INSERT INTO booking (date, time, price, email, AttractionID) VALUES (%s, %s, %s, %s, %s)"
                        val = (date, time, fee, email, AttractionID)
                    else:
                        sql = "UPDATE booking SET date = %s, time = %s, price = %s, AttractionID = %s WHERE email = %s"
                        val = (date, time, fee, AttractionID, email)
                    
                    myCursor.execute(sql, val)
                    cnx.commit()
                    
                    data = {"ok": True}
                    return jsonify(data), 200
        else:
            data = {"error": True, "message": "未登入系統，拒絕存取"}
            return jsonify(data), 403
    except jwt.ExpiredSignatureError:
        data = {"error": True, "message": "Token 已過期"}
        return jsonify(data), 403
    except jwt.InvalidTokenError:
        data = {"error": True, "message": "無效的 Token"}
        return jsonify(data), 403
    except Exception as e:
        data = {"error": True, "message": "伺服器內部錯誤"}
        return jsonify(data), 500

@Api_booking.route("/booking", methods=["GET"])
def get_booking():
    try:
        JWT_cookie = request.cookies.get("JWT")
        
        if JWT_cookie:
            getuser = jwt.decode(JWT_cookie, key, algorithms="HS256")
            email = getuser['email']
            
            with cnxpool.get_connection() as cnx:
                with cnx.cursor() as myCursor:
                    sql = "SELECT date, time, price, email, AttractionID FROM booking WHERE email = %s"
                    val = (email,)
                    myCursor.execute(sql, val)
                    records = myCursor.fetchone()
                    
                    if records is None:
                        data = {"data": None}
                        return jsonify(data)
                    else:
                        AttractionID = records[4]
                        date = records[0]
                        price = records[2]
                        time = records[1]
                        
                        sql = "SELECT name, address, images FROM attraction WHERE id = %s"
                        val = (AttractionID,)
                        myCursor.execute(sql, val)
                        records = myCursor.fetchone()
                        
                        output = ast.literal_eval(records[2])
                        booking_information = {
                            "attraction": {
                                "id": AttractionID,
                                "name": records[0],
                                "address": records[1],
                                "image": output[0],
                            },
                            "date": date,
                            "time": time,
                            "price": price
                        }
                        
                        data = {"data": booking_information}
                        return jsonify(data), 200
        else:
            data = {"error": True, "message": "未登入系統，拒絕存取"}
            return jsonify(data), 403
    except jwt.ExpiredSignatureError:
        data = {"error": True, "message": "Token 已過期"}
        return jsonify(data), 403
    except jwt.InvalidTokenError:
        data = {"error": True, "message": "無效的 Token"}
        return jsonify(data), 403
    except Exception as e:
        data = {"error": True, "message": "伺服器內部錯誤"}
        return jsonify(data), 500

@Api_booking.route("/booking", methods=["DELETE"])
def delete_booking():
    try:
        JWT_cookie = request.cookies.get("JWT")
        
        if JWT_cookie:
            getuser = jwt.decode(JWT_cookie, key, algorithms="HS256")
            email = getuser['email']
            
            with cnxpool.get_connection() as cnx:
                with cnx.cursor() as myCursor:
                    sql = "DELETE FROM booking WHERE email = %s"
                    val = (email,)
                    myCursor.execute(sql, val)
                    cnx.commit()
                    
                    data = {"ok": True}
                    return jsonify(data), 200
        else:
            data = {"error": True, "message": "未登入系統，拒絕存取"}
            return jsonify(data), 403
    except jwt.ExpiredSignatureError:
        data = {"error": True, "message": "Token 已過期"}
        return jsonify(data), 403
    except jwt.InvalidTokenError:
        data = {"error": True, "message": "無效的 Token"}
        return jsonify(data), 403
    except Exception as e:
        data = {"error": True, "message": "伺服器內部錯誤"}
        return jsonify(data), 500
