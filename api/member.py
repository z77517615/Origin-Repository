from flask import *
import jwt
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling
from decouple import config
from datetime import datetime, timedelta
import time

member = Blueprint('member', __name__)
key = os.getenv("JWT")
dt = datetime.now() + timedelta(seconds=30)   

load_dotenv()
cnxpool=pooling.MySQLConnectionPool(pool_name="mypool",
                                    pool_size=10,
                                    host=os.getenv("host"),
                                    password=os.getenv("password"),
                                    user=os.getenv("user"),
                                    database=os.getenv("database"),
                                    pool_reset_session=True
                                             )


# 取得使用者狀態
@member.route("/user",methods=["GET"])
def get_userdata():
    JWT_cookie = request.cookies.get("JWT")  
    if JWT_cookie:
        getuser=jwt.decode(JWT_cookie, key, algorithms="HS256")           
        response = make_response({
            "data": getuser
            })       
        return response
    else:
        response = make_response({
            "data": None
            })       
        return response



# 註冊
@member.route("/user",methods=["POST"])
def signup():
    try: 
        cnx=cnxpool.get_connection()
        mycursor=cnx.cursor()   
        data = request.json
        name=data["name"]
        email=data["email"]
        password=data["password"]
        sql = "SELECT id ,username, email, password FROM member WHERE email =%s"
        val=(email,)
        mycursor.execute(sql,val)
        records=mycursor.fetchone()
        if records == None:
            sql="INSERT INTO member (username,email,password) VALUES (%s, %s ,%s )"
            val=(name ,email ,password)
            mycursor.execute(sql,val)
            cnx.commit()
            response=make_response({
                "ok": True
                },200)
            return response
        else:
            response=make_response({
                "error": True, 
                "message": "註冊失敗，重複的 Email 或其他原因"
                 },400)
            return response
    except:
        response=make_response({
            "error": True, 
            "message": "伺服器內部錯誤"
            },500)
        return response

    finally:
        mycursor.close() 
        cnx.close()




# 登入
@member.route("/user",methods=["PATCH"])
def signin():
    try:
        cnx=cnxpool.get_connection()
        mycursor=cnx.cursor()   
        data=request.json
        email = data['email']
        password = data['password']
        sql = "SELECT id ,username, email, password FROM member WHERE email =%s AND password =%s"
        val=(email, password,)
        mycursor.execute(sql,val)
        records=mycursor.fetchone()
        if records :        
            response = make_response({
                "ok": True
                },200)
            user={
                "id":records[0],
                "name":records[1],
                "email":records[2],
                "exp": dt
            }
            Token = jwt.encode(user, key, algorithm="HS256")
            response.set_cookie("JWT", Token, expires=time.time()+6*60)
            return response
        else:
            response = make_response({
            "error": True,
            "message": "登入失敗，帳號或密碼錯誤或其他原因"
            },400)
            return response
    except:
        response = make_response({
            "error": True,
            "message": "伺服器內部錯誤"
            },500)
        return response
    finally:
        mycursor.close() 
        cnx.close()
    


# 登出
@member.route("/user",methods=["DELETE"])
def singout():   
    response = make_response({
        "ok": True
        },200)
    response.delete_cookie("JWT")
    return response