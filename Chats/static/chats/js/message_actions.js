function Create_message_outcoming(text, Time, id) {
    var message = document.createElement("div");
    message.setAttribute("class","outgoing_msg");
    message.setAttribute("id", id);
    var message_son = document.createElement("div");
    message_son.setAttribute("class", "sent_msg");
    var send_text = document.createElement("p");
    send_text.innerText = text;
    var time = document.createElement("span");
    time.setAttribute("class", "time_date");
    time.innerText = Time;
    message_son.appendChild(send_text);
    message_son.appendChild(time);
    message.appendChild(message_son);
    return message
}

function Create_message_incoming(text, pic, Time, id) {
    var message = document.createElement("div");
    message.setAttribute("class","incoming_msg");
    message.setAttribute("id", id);
    var img_div = document.createElement("div");
    img_div.setAttribute("class","incoming_msg_img");
    var img = document.createElement("img");
    img.setAttribute("src",pic);
    img.setAttribute("class", "avatar");
    img.setAttribute("alt", "Avatar");
    img_div.appendChild(img);
    var big_text_div = document.createElement("div");
    big_text_div.setAttribute("class","received_msg");
    var text_div = document.createElement("div");
    text_div.setAttribute("class","received_withd_msg");
    var main_text = document.createElement("p");
    var time = document.createElement("span");
    time.setAttribute("class", "time_date");
    time.innerText = Time;
    main_text.innerText = text;
    text_div.appendChild(main_text);
    text_div.appendChild(time);
    big_text_div.appendChild(text_div);
    message.appendChild(img_div);
    message.appendChild(big_text_div);
    return message
}

function Create_message(user, sender, text, pic, time, id) {
    m = Create_message_incoming(text, pic, time, id);
    if(sender == user){
         m = Create_message_outcoming(text, time, id);
    }
    lebron = document.getElementById('start');
    lebron.appendChild(m);
}

function Send_outcoming() {
    var inp = document.getElementById("inp");
    var text = inp.value;
    inp.value = '';
    var id = document.getElementsByClassName("chat_list active_chat")[0].id;
    var xml = new XMLHttpRequest();
    xml.open('GET', 'http://127.0.0.1:5000/sent_message?text=' + text+"&room="+id, true);
    xml.send();
}


function Print_messages(user, messages) {
    chat = document.getElementById("start");
    chat.innerHTML = '';
    for (i = 0; i < messages.length; i++) {
        message = messages[i];
        Create_message(user, message[2], message[1], message[6], message[5]+'|'+message[4], message[0]);
    }
}

function ApplyUpdate(user, messages) {
    chat = document.getElementById("start");
    for (i = 0; i < messages.length; i++) {
        message = messages[i];
        Create_message(user, message.SenderId, message.content, message.pic, message.time+'|'+message.date, message.id);
    }
}

function Update() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://127.0.0.1:5000/update?roomID="+Get_active_room()+"&lastTxt="+LastMessage(), true);
    xhttp.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200){
            if(xhttp.response != 'updated') {
                var usAndmes = JSON.parse(xhttp.response);
                ApplyUpdate(usAndmes.user, usAndmes.messages);
            }
            xhttp.open("GET", "http://127.0.0.1:5000/update?roomID="+Get_active_room()+"&lastTxt="+LastMessage(), true);
            xhttp.send();
        }
    };
    var messages;
    messages = document.getElementById('start');
    if(messages.innerText.length > 0){
        xhttp.send()
    }
}


