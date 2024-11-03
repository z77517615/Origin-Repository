from flask import *
import jwt
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling
from datetime import datetime, timedelta
import time
import bcrypt

member = Blueprint('member', __name__)

load_dotenv()
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

# 取得使用者狀態
@member.route("/user", methods=["GET"])
def get_userData():
    JWT_cookie = request.cookies.get("JWT")
    if JWT_cookie:
        try:
            getuser = jwt.decode(JWT_cookie, key, algorithms=["HS256"])
            response = make_response({"data": getuser})
        except jwt.ExpiredSignatureError:
            response = make_response({"data": None, "message": "Token has expired"}, 401)
        except jwt.InvalidTokenError:
            response = make_response({"data": None, "message": "Invalid token"}, 401)
    else:
        response = make_response({"data": None})
    return response

# 註冊
@member.route("/user", methods=["POST"])
def signup():
    try:
        cnx = cnxpool.get_connection()
        myCursor = cnx.cursor()
        data = request.json
        name = data["name"]
        email = data["email"]
        password = data["password"]
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        sql = "SELECT id FROM member WHERE email = %s"
        val = (email,)
        myCursor.execute(sql, val)
        records = myCursor.fetchone()
        if records is None:
            sql = "INSERT INTO member (username, email, password) VALUES (%s, %s, %s)"
            val = (name, email, hashed_password)
            myCursor.execute(sql, val)
            cnx.commit()
            response = make_response({"ok": True}, 200)
        else:
            response = make_response({"error": True, "message": "註冊失敗，重複的 Email 或其他原因"}, 400)
    except mysql.connector.Error as err:
        cnx.rollback()
        response = make_response({"error": True, "message": "伺服器內部錯誤"}, 500)
    finally:
        myCursor.close()
        cnx.close()
    return response

# 登入
@member.route("/user", methods=["PATCH"])
def signin():
    try:
        cnx = cnxpool.get_connection()
        myCursor = cnx.cursor()
        data = request.json
        email = data['email']
        password = data['password']

        sql = "SELECT id, username, email, password FROM member WHERE email = %s"
        val = (email,)
        myCursor.execute(sql, val)
        records = myCursor.fetchone()
        if records and bcrypt.checkpw(password.encode('utf-8'), records[3].encode('utf-8')):
            user = {
                "id": records[0],
                "name": records[1],
                "email": records[2],
                "exp": dt
            }
            token = jwt.encode(user, key, algorithm="HS256")
            response = make_response({"ok": True}, 200)
            response.set_cookie("JWT", token, expires=time.time() + 6 * 60)
        else:
            response = make_response({"error": True, "message": "登入失敗，帳號或密碼錯誤或其他原因"}, 400)
    except mysql.connector.Error as err:
        response = make_response({"error": True, "message": "伺服器內部錯誤"}, 500)
    finally:
        myCursor.close()
        cnx.close()
    return response

# 登出
@member.route("/user", methods=["DELETE"])
def signout():
    response = make_response({"ok": True}, 200)
    response.delete_cookie("JWT")
    return response
