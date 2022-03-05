import urllib.request as request
import json
import mysql.connector
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='attractions'
)

cursor = db.cursor()

url = 'taipei-attractions.json'

with open(url, mode='r', encoding='utf-8') as response:
    data = json.load(response)
attractions = data['result']['results']


for spot in attractions:
     picture=spot["file"]
     pic=picture.split("https:")  
     img=[]
     for i in range(1,len(pic)):
         images='https:'+pic[i]
         if images[-3:]=="JPG" or images[-3:]=="jpg" or images[-3:]=="png":
            img.append(images)
     
     sql = 'INSERT INTO attraction (name, category, description, address, transport, mrt, latitude, longitude, images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
     val = (spot['stitle'], spot['CAT2'], spot['xbody'], spot['address'], spot['info'], spot['MRT'], spot['latitude'], spot['longitude'], json.dumps(img))
   
     cursor.execute(sql, val)
     db.commit()