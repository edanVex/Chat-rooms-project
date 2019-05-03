from chat_DB_Handler import *

class User:

    def __init__(self, name, proPic, email, id):
        self.name = name
        self.proPic = proPic
        self.email = email
        self.id = id

    def Get_ProPic_Content(self):
        f = open(self.proPic, 'r')
        cont = f.readlines()
        f.close()
        return cont


class Room:

    def __init__(self, name, disc, users, id, pic, date, last = None):
        self.name = name
        self.disc = disc
        self.users = users
        self.id = id
        self.last = last
        self.src = pic
        self.date = date

    def Update_Users(self):
        chats = DB(r'C:/Users/Hagay/Desktop/pyCharm Projects/Chats/Chats-DB.db')
        users = chats.Get_Users_In_Room(self.id)
        chats.DB.close()
        users = users.split(',')
        for i in range(len(users)):
            users[i] = int(users[i])
        self.users = users

    def Update_Last(self):
        chats = DB(r'C:/Users/Hagay/Desktop/pyCharm Projects/Chats/Chats-DB.db')
        messgae = chats.Get_last_text(str(self.id))
        chats.DB.close()
        if(messgae):
            mess = Message(messgae[0], messgae[1], messgae[2], messgae[3], messgae[4], messgae[5])
            self.last = mess

    def __dict__(self):
        mess= self.last
        if mess and mess.time:
            return {'name':self.name, 'disc':self.disc, 'users':self.users, 'id':self.id,
                     'last':
                      {'id': mess.id, 'content':mess.content, 'SenderId':mess.SenderId, 'RoomId':mess.RoomId, 'date':mess.date, 'time':mess.time},
                     'src':self.src, 'date':self.date}
        elif mess and not mess.time:
            return {'name': self.name, 'disc': self.disc, 'users': self.users, 'id': self.id,
                    'last': {'id': mess.id, 'content': mess.content, 'SenderId': mess.SenderId, 'RoomId': mess.RoomId,
                             'date': mess.date, 'time': None}, 'src': self.src, 'date':self.date}
        else:
            return { 'name':self.name, 'disc':self.disc, 'users':self.users, 'id':self.id, 'last':None, 'src':self.src, 'date':self.date }



class Message:

    def __init__(self, id, content, SenderId, RoomId ,date ,time = None):
        self.id = id
        self.content = content
        self.SenderId = SenderId
        self.RoomId = RoomId
        self.date = date
        self.time = time


