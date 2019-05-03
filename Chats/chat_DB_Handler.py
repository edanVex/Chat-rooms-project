import sqlite3
from Const import *

def General_string(string):
    return '\''+string+'\''

class DB:

    def __init__(self, path):
        self.DB = sqlite3.connect(path)
        self.cursor = self.DB.cursor()

    def Create_Chat_Room(self, name, users_in_room, disc, path, date):
        self.cursor.execute('''
        INSERT INTO ChatRooms(Name, UsersInRoom, Discription, Picture, Date) VALUES(?,?,?,?,?)'''
                            , (name, users_in_room, disc, path, date))
        self.DB.commit()

    def Create_Message(self, room, text, sender, date, time):
        self.cursor.execute('''
        INSERT INTO Messages(Content, SenderId, RoomId, Date, Time) VALUES(?,?,?,?,?)'''
                            , (text, sender, room, date, time))
        self.DB.commit()
        return str(self.cursor.execute('''select MessageId from Messages where Date = "%s" and Content = "%s" and SenderId = %s''' %(str(date), text, sender)).fetchone())[1:-2]

    def Create_User(self, userName, password, email, profilePic):
        self.cursor.execute('''
        INSERT INTO Users(UserName, Password, Email, ProfilePic) VALUES(?,?,?,?)
        ''', (userName, password, email, profilePic))
        self.DB.commit()

    def Get_Users_In_Room(self, room):
        return str(self.cursor.execute('''
        SELECT UsersInRoom from ChatRooms
        WHERE Name = '''+room).fetchone())[2:-3]

    def Set_Users_In_Room(self, room, user):
        users=self.Get_Users_In_Room(General_string(room))+','+user
        self.cursor.execute('''
        UPDATE ChatRooms
        SET UsersInRoom = '''+'\''+users+'\''+
        '''WHERE Name = '''+'\''+room+'\'')
        self.DB.commit()

    def Get_Match(self, user, password):
        return self.cursor.execute('''
        select * from Users
        where UserName = '''+user+''' and Password = '''+ password).fetchone()

    def Get_chat(self, room):
        chat = self.cursor.execute('''
        select * from Messages
        WHERE RoomId = ''' + room)
        message = chat.fetchone()
        messages = []
        while(message != None):
            messages.append(list(message))
            message = chat.fetchone()
        return messages

    def Get_ProfilePic_By_Name(self, name):
        return str(self.cursor.execute('''
        select ProfilePic from Users
        where UserID =  ''' + '\"'+str(name)+'\"').fetchone())

    def Matching_rooms(self, exp, user):
        return self.cursor.execute('''
        select * from ChatRooms
        where Name like 
        '''+exp+''' and UsersInRoom like '''+user)

    def Get_last_text(self, room):
        messages = self.cursor.execute('''
        select * from Messages
        where RoomId = ''' + room)
        mess = messages.fetchone()
        last = mess
        if(mess != None):
            while(mess != None):
                last = mess
                mess = messages.fetchone()
            return list(last)
        else:
            return None

    def RoomsArray(self):
        rooms = self.cursor.execute('''
        select Name from ChatRooms
        ''')
        array = []
        room = rooms.fetchone()
        while(room != None):
            array.append(str(room)[2:-3])
            room = rooms.fetchone()
        return array

    def GetUserIDByUserName(self, name):
        return str(self.cursor.execute('''select UserID from Users where UserName = "%s"'''%(name)).fetchone())[1:-2]


    def LatestMessages(self, room, lastID):
        chat = self.cursor.execute('''
        select * from Messages
        where RoomId = %s and MessageId > %s''' %(room, lastID))
        message = chat.fetchone()
        messages = []
        while (message != None):
            messages.append(list(message))
            message = chat.fetchone()
        return messages

