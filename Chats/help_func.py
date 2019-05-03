from chat_DB_Handler import *
import hashlib
import json
from collections import namedtuple
from classes import *
import datetime



def General_string(string):
    return '\''+string+'\''

def Check_User_match(user, password):
    chats = DB(r'C:/Users/Hagay/Desktop/pyCharm Projects/Chats/Chats-DB.db')
    match = chats.Get_Match(General_string(user),General_string(password))
    chats.DB.close()
    return not(match == None)

def Create_Room(user, name, disc, path, date):
    chats = DB(r'C:/Users/Hagay/Desktop/pyCharm Projects/Chats/Chats-DB.db')
    chats.Create_Chat_Room(name,user,disc,path, date)
    chats.DB.close()

def Save_message(room, sender, text, date, time):
    chats = DB(r'C:/Users/Hagay/Desktop/pyCharm Projects/Chats/Chats-DB.db')
    chats.Create_Message(room, text, sender, date, time)
    chats.DB.close()

def Get_Chat_Room(room):
    chats = DB(r'C:/Users/Hagay/Desktop/pyCharm Projects/Chats/Chats-DB.db')
    messages = chats.Get_chat(room)
    for i in range(0,len(messages)):
        name = messages[i][2]
        pic = chats.Get_ProfilePic_By_Name(name)[2:-3]
        messages[i].append(pic)
    chats.DB.close()
    return messages

def find_rooms(exp, user):
    chats = DB(r'C:/Users/Hagay/Desktop/pyCharm Projects/Chats/Chats-DB.db')
    found = chats.Matching_rooms(General_string(exp+'%'), General_string('%'+user+'%'))
    matches = []
    match = found.fetchone()
    while(match != None):
        obj = list(match)
        match = Room(obj[1],obj[3], obj[2], obj[0], obj[4], obj[5])
        match.Update_Last()
        matches.append(match)
        match = found.fetchone()
    return matches


def GetRooms():
    chats = DB(r'C:/Users/Hagay/Desktop/pyCharm Projects/Chats/Chats-DB.db')
    arr = chats.RoomsArray()
    chats.DB.close()
    return arr

def AppendToRoom(room, user):
    chats = DB(r'C:/Users/Hagay/Desktop/pyCharm Projects/Chats/Chats-DB.db')
    chats.Set_Users_In_Room(room, user)
    chats.DB.close()

def ToDict(obj):
    j = obj.__dict__()
    return j

def LastMessObj(room):
    chats = DB(db_path)
    m = chats.Get_last_text(room)
    chats.DB.close()
    mess = Message(m[0], m[1], m[2], m[3], m[4], m[5])
    return mess

def GetLatestMessages(room, lastId):
    chats = DB(db_path)
    messages = chats.LatestMessages(room, lastId)
    for i in range(0, len(messages)):
        m = messages[i]
        mess = Message(m[0], m[1], m[2], m[3], m[4], m[5])
        pic = chats.Get_ProfilePic_By_Name(mess.SenderId)[2:-3]
        messages[i].clear()
        messages[i].append(mess)
        messages[i].append(pic)
    chats.DB.close()
    return messages