from flask import *
import ast
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling
from decouple import config

Attraction = Blueprint('Attraction', __name__)

load_dotenv()
cnxpool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,
    host=os.getenv("host"),
    password=os.getenv("password"),
    user=os.getenv("user"),
    database=os.getenv("database"),
    pool_reset_session=True
)

def get_attractions(page_index, keyword=""):
    cnx = cnxpool.get_connection()
    myCursor = cnx.cursor()
    try:
        if keyword:
            sql = "SELECT * FROM attraction WHERE name LIKE %s LIMIT 12 OFFSET %s"
            myCursor.execute(sql, (f"%{keyword}%", page_index))
        else:
            sql = "SELECT * FROM attraction LIMIT 12 OFFSET %s"
            myCursor.execute(sql, (page_index,))
        records = myCursor.fetchall()
        return records
    finally:
        myCursor.close()
        cnx.close()

@Attraction.route('/attractions')
def api_attractions():
    try:
        page = int(request.args.get('page', 0))
        page_index = page * 12
        next_page = page + 1
        keyword = request.args.get('keyword', "")

        records = get_attractions(page_index, keyword)
        results = []
        for record in records:
            output = ast.literal_eval(record[9])
            result = {
                "id": record[0],
                "name": record[1],
                "category": record[2],
                "description": record[3],
                "address": record[4],
                "transport": record[5],
                "mrt": record[6],
                "latitude": record[7],
                "longitude": record[8],
                "images": output
            }
            results.append(result)

        data = {
            "next_page": next_page if results else "null",
            "data": results
        }
        return jsonify(data)

    except Exception as e:
        return {
            "error": True,
            "message": "自訂的錯誤訊息"
        }, 500

@Attraction.route('/attraction/<int:variable>')
def attraction(variable):
    cnx = cnxpool.get_connection()
    myCursor = cnx.cursor()
    try:
        sql = "SELECT * FROM attraction WHERE id = %s"
        myCursor.execute(sql, (variable,))
        record = myCursor.fetchone()
        if record:
            output = ast.literal_eval(record[9])
            result = {
                "id": record[0],
                "name": record[1],
                "category": record[2],
                "description": record[3],
                "address": record[4],
                "transport": record[5],
                "mrt": record[6],
                "latitude": record[7],
                "longitude": record[8],
                "images": output
            }
            data = {"data": result}
            return jsonify(data)
        else:
            return {
                "error": True,
                "message": "Attraction not found"
            }, 404

    except Exception as e:
        return {
            "error": True,
            "message": "伺服器內部錯誤"
        }, 500

    finally:
        myCursor.close()
        cnx.close()
