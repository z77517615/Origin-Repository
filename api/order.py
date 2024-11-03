from flask import Blueprint, request, jsonify
import ast
import os
import requests
import json
import jwt
from dotenv import load_dotenv
from mysql.connector import pooling
from datetime import datetime, timedelta

load_dotenv()

order = Blueprint('order', __name__)
key = os.getenv("JWT_SECRET_KEY")
dt = datetime.now() + timedelta(days=1)

cnxpool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,
    host=os.getenv("DB_HOST"),
    password=os.getenv("DB_PASSWORD"),
    user=os.getenv("DB_USER"),
    database=os.getenv("DB_NAME"),
    pool_reset_session=True
)

@order.route("/orders", methods=["POST"])
def pay_order():
    JWT_cookie = request.cookies.get("JWT")
    if not JWT_cookie:
        return jsonify({"error": True, "message": "未登入系統，拒絕存取"}), 403

    try:
        getuser = jwt.decode(JWT_cookie, key, algorithms="HS256")
        email = getuser['email']
        name = getuser['name']
        
        cnx = cnxpool.get_connection()
        myCursor = cnx.cursor()
        
        orderData = request.get_json()
        url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
        order_number = datetime.now().strftime("%Y%m%d%H%M%S")
        contact = orderData['order']['contact']
        trip = orderData['order']['trip']
        attraction = trip['attraction']
        
        body = {
            "prime": orderData['prime'],
            "partner_key": os.getenv("PARTNER_KEY"),
            "merchant_id": os.getenv("MERCHANT_ID"),
            "details": "TapPay Test",
            "amount": orderData['order']['price'],
            "order_number": order_number,
            "cardholder": {
                "phone_number": contact['phone'],
                "name": contact['name'],
                "email": email,
            },
            "remember": True
        }
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": os.getenv("PARTNER_KEY")
        }
        
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response_status = response.json()
        
        if response_status["status"] == 0:
            sql = """
                INSERT INTO orders (date, time, price, email, payment, orderNumber, phone, name, attraction, attractionID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (trip['date'], trip['time'], orderData['order']['price'], email, 0, order_number, contact['phone'], contact['name'], attraction['name'], attraction['id'])
            myCursor.execute(sql, val)
            cnx.commit()
            
            sql = "DELETE FROM booking WHERE email=%s"
            myCursor.execute(sql, (email,))
            cnx.commit()
            
            return jsonify({"data": response_status}), 200
        else:
            return jsonify({"error": True, "message": "訂單建立失敗，輸入不正確或其他原因", "order_number": order_number}), 400
    except Exception as e:
        cnx.rollback()
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        myCursor.close()
        cnx.close()

@order.route("/orders/<order_number>", methods=["GET"])
def get_order(order_number):
    JWT_cookie = request.cookies.get("JWT")
    if not JWT_cookie:
        return jsonify({"error": True, "message": "未登入系統，拒絕存取"}), 403

    try:
        getuser = jwt.decode(JWT_cookie, key, algorithms="HS256")
        email = getuser['email']
        name = getuser['name']
        
        cnx = cnxpool.get_connection()
        myCursor = cnx.cursor()
        
        sql = "SELECT date, time, price, payment, orderNumber, phone, attraction, attractionID FROM orders WHERE orderNumber=%s"
        myCursor.execute(sql, (order_number,))
        orderData = myCursor.fetchone()
        
        if not orderData:
            return jsonify({"error": True, "message": "訂單不存在"}), 404
        
        attr_name = orderData[6]
        sql = "SELECT address, images FROM attraction WHERE name LIKE %s"
        myCursor.execute(sql, (f"%{attr_name}%",))
        attr_data = myCursor.fetchone()
        
        if not attr_data:
            return jsonify({"error": True, "message": "景點不存在"}), 404
        
        image = ast.literal_eval(attr_data[1])
        data = {
            "data": {
                "number": orderData[4],
                "price": orderData[2],
                "trip": {
                    "attraction": {
                        "id": orderData[7],
                        "name": orderData[6],
                        "address": attr_data[0],
                        "image": image[0]
                    },
                    "date": orderData[0],
                    "time": orderData[1]
                },
                "contact": {
                    "name": name,
                    "email": email,
                    "phone": orderData[5]
                },
                "status": orderData[3]
            }
        }
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        myCursor.close()
        cnx.close()
