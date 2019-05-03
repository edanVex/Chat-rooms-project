function Create_div(Class) {
    var div = document.createElement("div");
    div.setAttribute("class", Class);
    return div;
}

function Create_room(name, Text, pic, i, date){
    var Main = document.createElement("button");
    Main.setAttribute('class','chat_list');
    Main.setAttribute('onclick', 'request('+i+')');
    var semi = Create_div("chat_people");
    var img = Create_div("chat_img");
    var ib = Create_div("chat_ib");
    var head = document.createElement("h5");
    var text = document.createElement("p");
    var picture = document.createElement("img");
    var Date = document.createElement("span");
    Date.setAttribute('class', 'chat_date');
    Date.innerText = date;
    head.innerText = name;
    text.innerText = Text;
    head.appendChild(Date);
    ib.appendChild(head);
    ib.appendChild(text);
    picture.setAttribute("src", pic);
    picture.setAttribute("alt", "Avatar");
    picture.setAttribute("class", "avatar");
    img.appendChild(picture);
    semi.appendChild(img);
    semi.appendChild(ib);
    Main.appendChild(semi);
    Main.setAttribute("id", i);
    return Main;
}

function Create_list(chatRooms){
    var list = document.getElementById("list");
    list.innerHTML = '';
    var rooms = JSON.parse(chatRooms);
    if(rooms.length > 0){
        for(var i =0; i < rooms.length; i++){
            var room = rooms[i];
            var r;
            if(room.last != null){
                r = Create_room(room.name, room.last.content, room.src, room.id, room.date);}
            else{
                r = Create_room(room.name, 'No messages yet', room.src, room.id, room.date);}
            list.appendChild(r);
        }
    }
    else{
        list.innerText = 'No Rooms Found'
    }
}

function Create__list(chatRooms){
    var list = document.getElementById("list");
    list.innerHTML = '';
    if(chatRooms.length > 0){
        for(var i =0; i < chatRooms.length; i++){
            var room = chatRooms[i];
            var r;
            if(room.last != null){
                r = Create_room(room.name, room.last.content, room.src, room.id, room.date);}
            else{
                r = Create_room(room.name, 'No messages yet', room.src, room.id, room.date);}
            list.appendChild(r);
        }
    }
    else{
        list.innerText = 'No Rooms Found'
    }
}

function Generate_chat_rooms() {
    var input = document.getElementById("search");
    text = input.value;
    var r = new XMLHttpRequest();
    r.onreadystatechange = function (){
        if (this.readyState == 4 && this.status == 200) {
            Create_list(r.response)
        }};
    r.open("GET", "http://127.0.0.1:5000/get_rooms?exp="+text, true);
    r.send();
}

function Get_active_room() {
    var Element1 = document.getElementsByClassName("chat_list active_chat")[0];
    if(Element1 == undefined){return document.getElementById("list").firstElementChild.id;}
    else {return Element1.id;}
}


function request(id, flag=false){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://127.0.0.1:5000/messages?room="+id , true);
    xhttp.send();
    xhttp.onreadystatechange = function () {
        if(this.readyState == 4 && this.status == 200){
            if(!flag){
                var mesAndus = JSON.parse(xhttp.response);
                Show(id, mesAndus.user, mesAndus.messages);
            }
            else{
                var mesAndus = JSON.parse(xhttp.response);
                Show(id, mesAndus.user, mesAndus.messages, true);
            }
        }
    }
}

function requestAndWait(id, ){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://127.0.0.1:5000/messages?room="+id , false);
    xhttp.send();
    xhttp.onreadystatechange = function () {
        if(this.readyState == 4 && this.status == 200){
            alert(xhttp.response);
            var mesAndus = JSON.parse(xhttp.response);
            Show(id, mesAndus.user, mesAndus.messages)
        }
    }
}

function Show(id, user, messages, flag=false) {
    lastRoom = document.getElementsByClassName("chat_list active_chat")[0];
    if(lastRoom != undefined){
        lastRoom.setAttribute("class","chat_list");}
    room = document.getElementById(id);
    room.setAttribute("class","chat_list active_chat");
    Print_messages(user, messages);
    if(flag){
        Update();
    }
}

function DropDownlist() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://127.0.0.1:5000/DropDownRooms?room="+document.getElementById('myInput').value, true);
    closeSearch();
    xhttp.send()
}

function LastMessage() {
    var mes = document.getElementById('start').lastElementChild;
    var text = mes.id;
    return text;
}

