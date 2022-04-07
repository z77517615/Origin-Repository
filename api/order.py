from flask import *
import ast,os,requests,json,time,jwt
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling
from decouple import config
from datetime import datetime, timedelta


order = Blueprint('order', __name__)
key = os.getenv("JWT")
dt = datetime.now() + timedelta(days=1)   

load_dotenv()
cnxpool=pooling.MySQLConnectionPool(pool_name="mypool",
                                    pool_size=10,
                                    host=os.getenv("host"),
                                    password=os.getenv("password"),
                                    user=os.getenv("user"),
                                    database=os.getenv("database"),
                                    pool_reset_session=True
                                             )


@order.route("/orders",methods=["POST"])
def pay_order():
    JWT_cookie = request.cookies.get("JWT")
    if JWT_cookie:            
        getuser=jwt.decode(JWT_cookie, key, algorithms="HS256")
        email=getuser['email']
        name=getuser['name'] 
        try:
            cnx=cnxpool.get_connection()
            mycursor=cnx.cursor()   
            orderdata = request.get_json()
            url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
            order_number = datetime.now().strftime("%Y%m%d%H%M%S")
            name=orderdata['order']['contact']['name']
            phone_number=orderdata['order']['contact']['phone']
            amount=orderdata['order']['price']
            date=orderdata['order']['trip']['date']
            time=orderdata['order']['trip']['time']
            attraction=orderdata['order']['trip']['attraction']['name']
            attractionID=orderdata['order']['trip']['attraction']['id']
            print("ok-1")
            body = {
                "prime": orderdata['prime'],
                "partner_key": "partner_eKPaKE7j387Fao285CgnmCXyVuNW5AIiX0AvKBxxz7Sq3zgww2DMzWkM",
                "merchant_id": "zoecheng_ESUN",
                "details":"TapPay Test",
                "amount": amount,
                "order_number": order_number,
                "cardholder": {
                    "phone_number": phone_number,
                    "name": name,
                    "email": email,
                },
                "remember": True
            }
            print("ok-3")
            headers = {
                "Content-Type": "application/json",
                "x-api-key": "partner_eKPaKE7j387Fao285CgnmCXyVuNW5AIiX0AvKBxxz7Sq3zgww2DMzWkM"
            }
            print("ok-2")
            response = requests.post(url, data=json.dumps(body), headers=headers)
            response_status = response.json()
            print(response_status)
            if response_status["status"] == 0:
                print("ok")
                # 修改 order 紀錄已付款/booking未付款刪除
                sql= "INSERT INTO orders (date , time , price , email ,payment ,ordernumber , phone , name , attraction, attractionID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val=(date,time,amount,email,0,order_number,phone_number,name,attraction,attractionID)
                mycursor.execute(sql,val)
                cnx.commit()
                sql="DELETE FROM booking WHERE email=%s"
                val=(email,)
                mycursor.execute(sql,val)
                cnx.commit()
                data= {
                    "data" : response_status
                    }
                return jsonify(data), 200

            else:
                data= {
                   "error": True, 
                   "message": "訂單建立失敗，輸入不正確或其他原因", 
                   "order_number": order_number,
                   }
                return jsonify (data), 400
        except:
            data ={
                "error":True, 
                "message":"伺服器內部錯誤"
                }
            return jsonify (data), 500
        
        finally:
            mycursor.close() 
            cnx.close()  

    else:
        data={
        "error": True,
        "message": "未登入系統，拒絕存取"
        }
        return jsonify(data),403

 

@order.route("/orders/<order_number>",methods=["GET"])
def get_order(order_number):
    try:
        JWT_cookie=request.cookies.get("JWT") 
        if JWT_cookie:    
            getuser=jwt.decode(JWT_cookie, key, algorithms="HS256")
            email=getuser['email']
            name=getuser['name'] 
            cnx=cnxpool.get_connection()
            mycursor=cnx.cursor() 
            sql="SELECT date, time, price, payment, ordernumber, phone, attraction, attractionID from orders where ordernumber=%s"
            val=(order_number,)
            mycursor.execute(sql,val)
            orderdata=mycursor.fetchone()
            attr_name=orderdata[6]
            sql=f"SELECT address, images from attraction where name like ('%{attr_name}%')"
            mycursor.execute(sql)
            attr_data=mycursor.fetchone()
            image=ast.literal_eval(attr_data[1])
            data={
                "data": {
                    "number": orderdata[4],
                    "price": orderdata[2],
                    "trip": {
                    "attraction": {
                        "id": orderdata[7],
                        "name": orderdata[6],
                        "address": attr_data[0],
                        "image": image[0]
                    },
                    "date": orderdata[0],
                    "time": orderdata[1]
                    },
                    "contact": {
                    "name": name,
                    "email": email,
                    "phone": orderdata[5]
                    },
                    "status": orderdata[3]
                }            
            }
            return jsonify(data),200
                    
        else:
            data = {
                "error": True,
                "message": "未登入系統，拒絕存取"
                }
            return jsonify(data),400
    finally:
        mycursor.close() 
        cnx.close() 
            


