var Chat = {
    add_message: function(msg, role, type) {
        var time = Utils.format_date("HH:mm:ss");

        var conversation = document.getElementsByClassName("conversation")[0]
        var message_list = document.getElementsByClassName("message-list")

        if (type == "url") {
            msg = "<div class='wrap'>" +
                "<iframe id='chat-iframe' frameborder=0 src='" + msg +"'></iframe>" +
                " </div>";
        }

        if (type == "obj") {
            msg = "<div class='wrap'><table class='table' id='schedule'>" + 
                  "<thead><th>出發時間</th><th>抵達時間</th></thead>" +
                  Chat.create_table(msg) + "</table></div>"
        }

        var html = "<li class='message left'>" + 
                   "<div class='content bot arrow left'>" + msg + "</div>" +
                   "<div class='message-time'>" + time + "</div></li>"

        if (role == "user") {
            html = "<li class='message right'>" + 
                   "<div class='content user arrow right'>" + msg + "</div>" +
                   "<div class='message-time'>" + time + "</div></li>"

        }

        $(message_list).append(html);
        // scroll to the bottom
        console.log(conversation.scrollHeight)
        conversation.scrollTop = conversation.scrollHeight;
    },

    do_add_message: function(event) {
        var text = Utils.escape_html($("#text-field").val());

        if (!text) { return; }

        Chat.add_message(text, "user", "str");

        Chat.ask_question(text, function(resp, msg_type) {
            Chat.add_message(resp, "bot", msg_type);
        });


        $("#text-field").val("");
    },

    ask_question: function(text, callback) {
        $.post('/foo', { "raw_text": text }, function(resp) {

            if (resp == null) {
                callback("我沒聽清楚，請再說一遍。");
            }

            resp = JSON.parse(resp);

            if (resp['task'] != null && resp['dialogue_state'] == 'completed') {
                console.log("Conversation Completed");

                Chat.request_schedule(resp["task"], function(url) {
                    callback(url, "obj"); 
                });
            }

            callback(resp["dialogueReply"], "str");
        });
    },

    init_dialogue: function(callback) {
        $.post('/init', {}, function(resp) {
            
            if (resp == null) {
                callback("我沒聽清楚，請再說一遍。");
            }

            resp = JSON.parse(resp);
            
            callback(resp["dialogueReply"], "str");
        });
    },


    request_schedule: function(payload, callback) {
        $.post( '/get_schedule', { "data": JSON.stringify(payload) }, function(obj) {
            if (obj== null) { console.log("nothing") }
            console.log(obj)
            callback(obj);
        });
    },

    create_table: function(json_obj) {
        obj = $.parseJSON(json_obj);
        body = $('<tbody></tbody>');
        $.each(obj, function(i, item) {
            row = $('<tr></tr>');
            row.append(
                $('<td></td>').text(item.start),
                $('<td></td>').text(item.arrival)
            ) 
            body.append(row);
        });

        return body.html()
    },

    load: function() {

        Chat.init_dialogue(function(resp) {
            if (resp == null) {
                Chat.add_message("您好，請問您需要什麼服務？", "bot", "str");
            }
            else {
                Chat.add_message(resp, "bot", "str");
            }
        });


        $("#speaker")[0].play();

        $("#text-field").keypress(function(e) {
            var text = Utils.escape_html($("#text-field").val())

            if (e.keyCode === 13 && text != "") {
                Chat.do_add_message();
            } 
        });

        $("#send-button").click(Chat.do_add_message);

        $("#speak-button").click(startDictation);
    }
}

$(document).ready(function () {
    Chat.load();
});
