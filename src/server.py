""" server.py
Setup flask server and parse/send requests
"""
import os
import re
import flask
import psycopg2
import requests
from flask import render_template, request

# Parse data/URLs
DATABASE_URL = os.environ['DATABASE_URL']
BLOG_URL = "http://nefault1s.online/Blog.php"

PASSWORDS = { # Might be added in the database
"bubbles": ("132", "You've just received the toy bubble maker!#This will be fun for all chao!6"),
"sola1st": ("132", "You've received the dev's first chao!#Meet Sola the chao; raised by Sonic!#Take good care of her!2"),
"concept of love": ("132", "You've received Beat the Chao!#Beat is one musical prodigy.#Treat this chao with great care!5"),
"joyconboyz": ("132", "You've received the special EWN Chao!#R.I.P Desmond#J O Y C O N B O Y Z F O R E V E R1"), # RIP Etika
#"test3": ("132", "This is a test value.3"), # White chao
#"test4": ("132", "This is a test value.4"), # TV
#"test7": ("132", "This is a test value.7"), # ORCA
} 

# Connect to database
con = psycopg2.connect(DATABASE_URL, sslmode='require')
CUR = con.cursor()


@app.route('/')
def index():
    """ Displays the index page accessible at '/' """
    return render_template('index.html')

@app.route('/blog', methods=['POST'])
def blog():
    """ Handle and parse blog/news board requests """
    over_view = request.form["over_view"]
    get_id = request.form["get_id"]
    #print(f"over:{over_view}; id:{get_id}")
    if over_view == "1":
        titles = []
        CUR.execute("SELECT count(*) FROM public.announcements;") # Get cardinal
        raw_count = CUR.fetchall()
        card = raw_count[0][0]
        #print(f"card:{card}")
        for i in range(1, card+1):
            CUR.execute(f"SELECT * FROM public.announcements WHERE id={i};")
            raw_data = CUR.fetchall()
            #print(f"raw:{raw_data}; titles:{titles}")
            titles.append(raw_data[0][1])
        titles.reverse()
        titles_txt = ''.join(titles)
        return titles_txt # Title list
    else:
        CUR.execute(f"SELECT * FROM public.announcements WHERE id={get_id};")
        raw_data = CUR.fetchall()
        msg = raw_data[0][2]
        return msg

@app.route('/news_count', methods=['POST'])
def news_count():
    """ Return the number of news available """
    CUR.execute("SELECT count(*) FROM public.announcements;") # Get cardinal
    raw_count = CUR.fetchall()
    return str(raw_count[0][0])

@app.route('/update', methods=['POST'])
def update():
    """ Fetch updates """
    win_url = "https://github.com/Kugge/Chao-Resort-Island-X/releases/latest/download/Chao.Resort.Island.zip"
    mac_url = "https://github.com/Kugge/Chao-Resort-Island-X/releases/latest/download/Chao.Resort.Island.Mac.zip"
    req = requests.get("https://raw.githubusercontent.com/Kugge/Chao-Resort-Island-X/master/Version.txt")
    ver = re.search(r"OVERSION=([0-9]*)\r", req.text).group(1)
    mod_ver = re.search(r"XVERSION=([0-9]*)\r", req.text).group(1)
    os = request.form["os_g_version"]
    if os == "windows":
        # mod_ver was originally random size, so I replaced it by mod version.
        # 110 = Min version compatible with auto update.
        return ver + "[" + win_url + "]" + mod_ver + "{110"
    elif os == "mac" or os == "ios":
        return ver + "[" + mac_url + "]" + mod_ver + "{110"
    else:
        return ""

@app.route('/secret', methods=['POST'])
def secret():
    """ Handle online secrets in the game """
    ver = request.form["submit_version"]
    secret = request.form["secret"]
    print(secret)
    if ver == '-1':
        if secret in PASSWORDS:
            return PASSWORDS[secret][1]
        else:
            return "R"
    else:
        if secret in PASSWORDS:
            return PASSWORDS[secret][0]
        else:
            return "132"


if __name__ == '__main__':
    # Run the app
    app.debug=True
    port = int(os.environ.get('PORT', 5000))
    app.run(threaded=True, port=port, host='0.0.0.0')
