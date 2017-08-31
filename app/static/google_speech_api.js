var final_transcript = '';
var recognizing = false;

if ('webkitSpeechRecognition' in window) {

    var recognition = new webkitSpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;

    speak_btn = $("#speak-button")[0];

    recognition.onstart = function() {
        $("#speak-button")[0].innerText="Stop";
        recognizing = true; 
    };

    recognition.onerror = function(event) {
        console.log("dictate error, reason: " + event.error);
    };

    recognition.onend = function() {
        $("#speak-button")[0].innerText="Speak";
        recognizing = false;
    };

    recognition.onresult = function(event) {
        var interim_transcript = '';

        for (var i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                final_transcript += event.results[i][0].transcript;
            }
        }

        final_transcript = capitalize(final_transcript);

        $("#text-field").val(final_transcript);

        Chat.do_add_message(final_transcript);

        recognition.stop();
    };
}

function capitalize(s) {
    return s.replace(s.substr(0,1), function(m) { return m.toUpperCase(); });
}

function startDictation(event) {
    if (recognizing) {
        recognition.stop();
        return;
    }

    final_transcript = '';
    recognition.lang = 'cmn-Hant-TW';
    recognition.start();
}
/*
function ask_question(raw_text) {
    $.post( '/foo', {"raw_text" : final_transcript}, function(response) {  
	console.log(response);
        if (response == null) { add_string_in_tags("p", "系統:  我沒聽清楚，請再說一遍") }

        response = JSON.parse(response);


        add_string_in_tags("p", "系統: " + response["dialogueReply"]);

        if (response["dialogue_state"] == 'completed') { 
            get_schedule(response["task"]);
            return recognition.stop();
        }

        startDictation(event);
    })
}

function get_schedule(data) { 
    $.post( '/get_schedule' , { "data":  JSON.stringify(data) }, function(url) {
        console.log(url);
        if (url == "None") { return add_string_in_tags("p", "系統:  查無相關資料"); }
        $( '#schedule_list' ).attr('src', url);
    });
}

*/
