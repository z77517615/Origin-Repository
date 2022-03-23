from flask import Flask, Blueprint, session, request, jsonify
import ast
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling
from decouple import config

member = Blueprint('member', __name__)

load_dotenv()
cnxpool=pooling.MySQLConnectionPool(pool_name="mypool",
                                    pool_size=10,
                                    host=os.getenv("host"),
                                    password=os.getenv("password"),
                                    user=os.getenv("user"),
                                    database=os.getenv("member"),
                                    pool_reset_session=True
                                             )


# 取得使用者狀態
@member.route("/user",methods=["GET"])
def get_userdata():
    if "user" in session:
        getuser = session["user"]            
        data = {
            "data": getuser
            }       
        return data
    else:
        data = {
            "data": None
            }       
        return data



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
        print(records)
        if records == None:
            sql="INSERT INTO member (username,email,password) VALUES (%s, %s ,%s )"
            val=(name ,email ,password)
            mycursor.execute(sql,val)
            cnx.commit()
            data={
                "ok": True
                } 
            session["user"]={
            "name":name,
            "email":email,
            "passswod":password
            }        
            return data
        else:
            data={
                "error": True, 
                "message": "信箱已經被註冊"
                 }       
            return data
    except:
        data={
            "error": True, 
            "message": "伺服器內部錯誤"
            }     
        return data

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
            data = {
                "ok": True
                },200
            session["user"]={
                "id":records[0],
                "name":records[1],
                "email":records[2]
            }
            return data
        else:
            data = {
            "error": True,
            "message": "登入失敗，帳號或密碼輸入錯誤"
            },400  
            return data
    except:
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
            }
        return data
    finally:
        mycursor.close() 
        cnx.close()
    


# 登出
@member.route("/user",methods=["DELETE"])
def singout():
    session.pop("user",None)
    data = {
        "ok": True
        }
    return data