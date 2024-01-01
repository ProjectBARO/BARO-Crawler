import os, urllib.parse, requests, pymysql

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

conn = pymysql.connect(
    host=MYSQL_HOST,
    port=int(MYSQL_PORT),
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    db=MYSQL_DATABASE,
    charset='utf8mb4'
)

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search?"
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
params = {
    "key": YOUTUBE_API_KEY,
    "part": "snippet",
    "maxResults": 30,
    "q": "거북목%7C스트레칭%7C",
    "type": "video",
    "videoDuration" : "medium",
}

responses = requests.get(YOUTUBE_API_URL + urllib.parse.urlencode(params)).json()

data = [(response["id"]["videoId"], response["snippet"]["title"], response["snippet"]["thumbnails"]["medium"]["url"]) for response in responses["items"]]

with conn.cursor() as cursor:
    sql = """
        INSERT INTO videos
        (video_id, title, thumbnail_url)
        VALUES (%s, %s, %s)
    """
    cursor.executemany(sql, data)
conn.commit()

conn.close()