import json
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='attractions'
    )

def load_data_from_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as response:
        return json.load(response)

def extract_images(picture):
    pic = picture.split("https:")
    img = []
    for i in range(1, len(pic)):
        images = 'https:' + pic[i]
        if images.lower().endswith(("jpg", "png", "JPG")):
            img.append(images)
    return img

def insert_attraction(cursor, spot, images):
    sql = '''
    INSERT INTO attraction (name, category, description, address, transport, mrt, latitude, longitude, images)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    val = (
        spot['stitle'], spot['CAT2'], spot['xbody'], spot['address'], 
        spot['info'], spot['MRT'], spot['latitude'], spot['longitude'], 
        json.dumps(images)
    )
    cursor.execute(sql, val)

def main():
    url = 'taipei-attractions.json'
    data = load_data_from_file(url)
    attractions = data['result']['results']

    try:
        with get_db_connection() as db:
            cursor = db.cursor()
            for spot in attractions:
                images = extract_images(spot["file"])
                insert_attraction(cursor, spot, images)
            db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    main()