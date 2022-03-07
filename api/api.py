from flask import *
import ast
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling

Attraction = Blueprint('Attraction', __name__)

load_dotenv()
cnxpool=pooling.MySQLConnectionPool(pool_name="mypool",
                                    pool_size=3,
                                    host=os.getenv("host"),
                                    password=os.getenv("password"),
                                    user=os.getenv("user"),
                                    database=os.getenv("database"),
                                    pool_reset_session=True
                                             )



@Attraction.route('/attractions')
def api_attractions():
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
            return records        
    
    try:
        cnx=cnxpool.get_connection()
        mycursor=cnx.cursor()
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
                    mycursor.close() 
                    cnx.close()          
                    return {
                        "next_page": "null",
                        "data":results
                        }
                else:
                    mycursor.close() 
                    cnx.close()
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
                    mycursor.close()  
                    cnx.close()          
                    return {
                        "next_page": "null",
                        "data":results
                        }
                else:
                    mycursor.close() 
                    cnx.close()
                    return {
                    "next_page": next_page,
                    "data":results
                    }
    
    except:
        mycursor.close() 
        cnx.close()
        return {
        "error": True,
        "message": "自訂的錯誤訊息"
        },500


@Attraction.route('/attraction/<variable>')
def attration(variable):
    cnx=cnxpool.get_connection()
    mycursor=cnx.cursor()
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
            mycursor.close() 
            cnx.close()
            return {
                    "data":result
                    }
            
    except:
        mycursor.close() 
        cnx.close()
        return {
        "error": True,
        "message": "伺服器內部錯誤"
        }, 500


