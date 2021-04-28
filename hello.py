from flask import *
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)



@app.route("/register")
def register():
    a = json.loads(request.args["0"])
    print(a["birthday"])
    if a["birthday"]:
        a["birthday"] = a["birthday"].split("T")[0]
    db = pymysql.connect(host='localhost', user='root', password='', database='webs')
    cursor = db.cursor()
    try:
        if a["birthday"]:
            cursor.execute("insert into user (u_username, u_password, u_name, u_birthday, u_tel, u_email) "
                       "values ('%s','%s','%s','%s','%s','%s');"
                       % (a['username'], a['password'], a['nickname'], a['birthday'], a['tel'], a['email']))
        else:
            cursor.execute("insert into user (u_username, u_password, u_name, u_birthday, u_tel, u_email) "
                       "values ('%s','%s','%s',Null,'%s','%s');"
                       % (a['username'], a['password'], a['nickname'], a['tel'], a['email']))
        db.commit()
        data = cursor.fetchall()
        db.close()
        return str(data), 200, {"ContentType": "application/json"}
    except:
        db.rollback()
    return "", 666, {"ContentType": "application/json"}


@app.route("/login")
def login():
    a = json.loads(request.args["0"])
    db = pymysql.connect(host='localhost', user='root', password='', database='webs')
    try:
        cursor = db.cursor()
        cursor.execute("select * from user where u_username = '%s' and u_password = '%s';"
                       % (a['username'], a['password']))
        db.commit()
        data = cursor.fetchall()
        db.close()
        return str(data), 200, {"ContentType": "application/json"}
    except:
        db.rollback()
    return "", 666, {"ContentType": "application/json"}   

@app.route("/getmessages")
def getmessages():
    db = pymysql.connect(host='localhost', user='root', password='', database='webs')
    try:
        cursor = db.cursor()
        cursor.execute("select * from messages;")
        db.commit()
        data = cursor.fetchall()
        db.close()
        return str(data), 200, {"ContentType": "application/json"}
    except:
        db.rollback()
    return "", 666, {"ContentType": "application/json"}

@app.route("/sendmessage")
def sendmessage():
    a = json.loads(request.args["0"])
    db = pymysql.connect(host='localhost', user='root', password='', database='webs')
    try:
        cursor = db.cursor()
        cursor.execute("insert into messages (m_sender, m_sendtime, m_message) values ('%s','%s','%s');"
                       % (a['sender'], a['sendtime'], a['content']))
        db.commit()
        cursor.execute("select * from messages;")
        db.commit()
        data = cursor.fetchall()
        db.close()
        return str(data), 200, {"ContentType": "application/json"}
    except:
        db.rollback()
    return "", 666, {"ContentType": "application/json"}


if __name__ == "__main__":
    app.run()
