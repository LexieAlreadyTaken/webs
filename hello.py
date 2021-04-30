from flask import *
import pymysql
from flask_cors import CORS
import re

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

@app.route('/upload', methods=['POST'])
def upload():
    print("here")
    print(request.files)
    f = request.files.to_dict()['file']
    print(f)
    upload_path = 'C:\\store\\'+f.filename  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
    print(upload_path)
    f.save(upload_path)
    return "OKAY!", 200, {"ContentType": "application/json"}

    
@app.route('/editinfo', methods=['POST'])
def edifinfo():
    a = json.loads(request.form["params"])
    if a["birthday"]:
        a["birthday"] = a["birthday"].split("T")[0]
    db = pymysql.connect(host='localhost', user='root', password='', database='webs')
    cursor = db.cursor()
    data = ""
    try:
        if a["birthday"]:
            cursor.execute("update user set u_birthday=%s" % a['birthday'])
        if a["nickname"]:
            cursor.execute("update user set u_name=%s" % a['nickname'])
        if a["tel"]:
            cursor.execute("update user set u_tel=%s" % a['tel'])
        if a["email"]:
            cursor.execute("update user set u_email=%s" % a['email'])
        if a["birthday"] or a["nickname"] or a["tel"] or a["email"]:
            db.commit()
            data = cursor.fetchall()
            db.close()
        print(request.files)
        f = request.files.to_dict()['file']
        upload_path = 'C:\\store\\avatar\\'+a['username']+"."+f.filename.split('.')[-1]
        print(upload_path)
        f.save(upload_path)
        return str(data), 200, {"ContentType": "application/json"}
    except:
        db.rollback()
    return str(data), 200, {"ContentType": "application/json"}

@app.route("/gettest")
def gettest():
    f = open("test1.txt", "r", encoding="utf-8")
    lines = f.readlines()
    result = {}
    j = 0
    for i in range(0, len(lines)):
        a = re.findall("(.+) 【(.+)】", lines[i])
        print(a)
        if a:
            temptemp = {}
            answer = ""
            while True:
                if i+1 >= len(lines):
                    break
                b = re.findall("([A-Z]) (.+)", lines[i+1])
                print(b)
                if not b:
                    answer = lines[i+1]
                    break
                temptemp[b[0][0]] = b[0][1]
                i = i+1
            temp = {"问题":a[0][1], a[0][0]: temptemp, "答案":answer}
            result[j] = temp
            j = j+1
    f.close()
    return json.dumps(result), 200, {"ContentType": "application/json"}

if __name__ == "__main__":
    app.run()
