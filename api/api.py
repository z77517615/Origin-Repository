from flask import Flask
from flask import  Blueprint
from flask import session
from flask import request
import ast
from flask import session
from flask import request
from flask import redirect
from flask import render_template
import mysql.connector 
from mysql.connector import pooling

dbconfig={"host":"localhost",
          "user":'root',
          'password':'password',
          'database':'attractions'  }

cnxpool=mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool",
                                                    pool_size=3,
                                                    **dbconfig)

cnxpool.set_config(**dbconfig)
cnx1=cnxpool.get_connection()
mycursor=cnx1.cursor()

Attraction = Blueprint('Attraction', __name__)

def select(page_index, keyword=""):
    if keyword =="":
        sql= f"select * from attraction limit 12 offset {page_index}"
        mycursor.execute(sql)
        records=mycursor.fetchall()
        return records

    else:
        sql= f"select * from attraction where name like ('%{keyword}%') limit 12 offset {page_index}"
        mycursor.execute(sql)
        records=mycursor.fetchall()
        print(records)
        return records


@Attraction.route('/attractions')
def api_attractions():
    try:
        if request.args.get('page'):
            page = int(request.args.get('page'))
            page_index = page * 12
            next_page = page + 1

            if request.args.get('keyword'):
                keyword =request.args.get('keyword')
                records=select(page_index,keyword)
                results=[]
                for i in range(0,len(records)):
                    str=records[i][9]
                    output=ast.literal_eval(str)
                    result={
                        "id": records[i][0],
                        "name":records[i][1],
                        "category":records[i][2],
                        "description": records[i][3],
                        "address":records[i][4],
                        "transport": records[i][5],
                        "mrt": records[i][6],
                        "latitude": records[i][7],
                        "longitude": records[i][8],
                        "images":output
                    }  
                    results.append(result)
                if results == []:             
                    return {
                        "next_page": "null",
                        "data":results
                        }
                else:
                    return {
                    "next_page": next_page,
                    "data":results
                    }

            else:
                records=select(page_index)
                results=[]
                for i in range(0,len(records)):
                    str=records[i][9]
                    output=ast.literal_eval(str)
                    result={
                        "id": records[i][0],
                        "name":records[i][1],
                        "category":records[i][2],
                        "description": records[i][3],
                        "address":records[i][4],
                        "transport": records[i][5],
                        "mrt": records[i][6],
                        "latitude": records[i][7],
                        "longitude": records[i][8],
                        "images":output
                    }  
                    results.append(result)
                if results == []:             
                    return {
                        "next_page": "null",
                        "data":results
                        }
                else:
                    return {
                    "next_page": next_page,
                    "data":results
                    }
    
    except:
        return {
        "error": True,
        "message": "自訂的錯誤訊息"
        },500

@Attraction.route('/attraction/<variable>')
def attration(variable):
    try:
        if variable: 
            sql= f"select * from attraction where id = {variable}"
            mycursor.execute(sql)
            records=mycursor.fetchone()
            str=records[9]
            output=ast.literal_eval(str)
            result={
                "id": records[0],
                "name":records[1],
                "category":records[2],
                "description": records[3],
                "address":records[4],
                "transport": records[5],
                "mrt": records[6],
                "latitude": records[7],
                "longitude": records[8],
                "images":output
            }  
            return {
                    "data":result
                    }
            
    except:
        return {
        "error": True,
        "message": "伺服器內部錯誤"
        }, 500
cnx1.close()
