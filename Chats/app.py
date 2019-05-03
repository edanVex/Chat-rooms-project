import json
from flask import render_template, make_response, request, Flask, jsonify
import hashlib
from werkzeug.utils import secure_filename
from chat_DB_Handler import *
import shutil
import os
from help_func import *
from Const import *
import datetime


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = images_path


@app.route('/', methods=['GET', 'POST'])
def login():
    if(len(request.args) == 0):
        if len(request.cookies) == 0:
            return render_template('login.html', message='')
        else:
            passw = request.cookies.get('password')
            user = request.cookies.get('user')
            if Check_User_match(user, passw):
                return render_template('chats.html',id='',messages=SendRoom(user),user=user, rooms=GetRooms(), message="")
            else:
                return render_template('login.html', message='')
    else:
        if len(request.cookies) == 0:
            pssw = request.values.get('pass')
            user = request.values.get('user')
            pssw = str(pssw).encode('utf-8')
            passw = hashlib.md5(pssw).hexdigest()
            if Check_User_match(user, passw):
                resp = make_response(render_template('chats.html',id='',messages=SendRoom(user),user=user, rooms=GetRooms(), message=""))
                resp.set_cookie('user', user, max_age=datetime.datetime.now().second + (10 * 365 * 24 * 60 * 60))
                resp.set_cookie('password', passw, max_age=datetime.datetime.now().second + (10 * 365 * 24 * 60 * 60))
                return resp
            else:
                return render_template('login.html', message='wrong username or password')
        else:
            passw = request.cookies.get('password')
            user = request.cookies.get('user')
            if Check_User_match(user, passw):
                return render_template('chats.html', id='', messages=SendRoom(user), user=user, rooms=GetRooms(), message="")
            else:
                return render_template('login.html', message='')




@app.route('/register', methods=['GET', 'POST'])
def register():
    if(request.method == 'GET'):
        return render_template('register.html')
    else:
        user_data = request.values
        print(user_data)
        print('user')
        pic = images_path+user_data.get('name')+".jpg"
        name = user_data.get('name')
        email = user_data.get('email')
        password = user_data.get('password')
        password = str(password).encode('utf-8')
        password = hashlib.md5(password).hexdigest()
        try:
            chats = DB(r'C:/Users/Hagay/Desktop/pyCharm Projects/Chats/Chats-DB.db')
            chats.Create_User(name,password,email,pic)
            chats.DB.close()
            f = request.files['file']
            f.save(secure_filename(f.filename))
            path = server_path + f.filename
            shutil.copyfile(path, server_path+images_path + name + '.' +f.filename.split('.')[1])
            os.remove(server_path + f.filename)
            re = make_response(render_template('chats.html', rooms=GetRooms(), messages=SendRoom(name)), user=name)
            re.set_cookie('user', name, max_age=datetime.datetime.now().second + (10 * 365 * 24 * 60 * 60))
            re.set_cookie('password', password, max_age=datetime.datetime.now().second + (10 * 365 * 24 * 60 * 60))
            return re
        except sqlite3.IntegrityError as e:
            return render_template('register.html', message="This email is already in use")



@app.route('/sent_message', methods=['GET'])
def Catch_Meaage():
    text = request.values.get('text')
    RoomId = request.values.get('room')
    date = datetime.datetime.now()
    chats = DB(db_path)
    SenderId = chats.GetUserIDByUserName(request.cookies.get('user'))
    id = chats.Create_Message(RoomId, text, SenderId, date.date(), str(date.hour)+":"+str(date.minute))
    chats.DB.close()
    date = datetime.datetime.now()
    return json.dumps({'date':str(date.date())+"|"+str(date.hour)+":"+str(date.minute),'id':id})


@app.route('/get_rooms', methods=['GET'])
def RoomsSerachBar():
    exp = request.values.get('exp')
    objList = find_rooms(exp, request.cookies.get('user'))
    jsonList = []
    for obj in objList:
        jsonList.append(ToDict(obj))
    return json.dumps(jsonList)


@app.route('/messages', methods=["GET"])
def Get_Messages():
    id = request.values.get('room')
    messages = Get_Chat_Room(id)
    chats = DB(db_path)
    UserId = chats.GetUserIDByUserName(request.cookies.get('user'))
    chats.DB.close()
    return json.dumps({'messages':messages, 'user':UserId})



@app.route('/CreateRoom', methods=['GET', 'POST'])
def Create_ROom():
    if request.method == 'POST':
        date = datetime.datetime.now()
        room_data = request.values
        f = request.files['file']
        new = server_path + rooms_path + room_data.get('Name') + '.' + f.filename.split('.')[1]
        try:
            Create_Room(request.cookies.get('user'), room_data.get('Name'), room_data.get('dsc'), rooms_path + room_data.get('Name') + '.' + f.filename.split('.')[1], date.date())
            f.save(secure_filename(f.filename))
            old = server_path + f.filename
            shutil.copyfile(old, new)
            os.remove(old)
            return render_template('chats.html', rooms=GetRooms(), messages=SendRoom(request.cookies.get('user')), user=request.cookies.get('user'))
        except sqlite3.IntegrityError as e:
            render_template('chats.html', rooms=GetRooms(), messages=SendRoom(request.cookies.get('user')), user=request.cookies.get('user'), message="this room name is already exsist")


@app.route('/DropDownRooms', methods=['GET'])
def RoomDropDownList():
    room = request.values.get('room')
    user = request.cookies.get('user')
    AppendToRoom(room,user)
    return 'OK'


@app.route('/update', methods=['GET'])
def SendMissingMessages():
    RoomID = request.values.get('roomID')
    text = request.values.get('lastTxt')
    message = LastMessObj(RoomID)
    chats = DB(db_path)
    UserId = chats.GetUserIDByUserName(request.cookies.get('user'))
    chats.DB.close()
    if(str(message.id) == text):
        return 'updated'
    else:
        messages = []
        for mess in GetLatestMessages(RoomID, text):
            dict1 = mess[0].__dict__
            dict2 = {'pic':mess[1]}
            message = {**dict1, **dict2}
            messages.append(message)
        print(messages)
        return json.dumps({'user': UserId,'messages':messages})



if __name__ == '__main__':
    app.run()

def SendRoom(user):
    exp = ''
    objList = find_rooms(exp, user)
    jsonList = []
    for obj in objList:
        jsonList.append(ToDict(obj))
    return json.dumps(jsonList)
