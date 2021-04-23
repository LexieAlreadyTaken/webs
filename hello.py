from flask import *
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

"""
@app.route("/")
def redirect():
    return redirect(url_for("login"))

"""


@app.route("/register")
def login():
    a = json.loads(request.args["0"])
    a["birthday"] = a["birthday"].split("T")[0]
    if a['tel'] == '':
        a['tel'] = 0
    db = pymysql.connect(host='localhost', user='root', password='', database='webs')
    cursor = db.cursor()
    try:
        cursor.execute("insert into user (u_username, u_password, u_name, u_birthday, u_tel, u_email)"
                       "values ('%s','%s','%s','%s','%s','%s');"
                       % (a['username'], a['password'], a['nickname'], a['birthday'], a['tel'], a['email']))
        db.commit()
    except:
        db.rollback()
    data = cursor.fetchall()
    db.close()
    return str(data), 200, {"ContentType": "application/json"}


if __name__ == "__main__":
    app.run()
