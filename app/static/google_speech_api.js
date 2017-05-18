var final_transcript = '';
var recognizing = false;

if ('webkitSpeechRecognition' in window) {

    var recognition = new webkitSpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = function() {
	$("#start_button")[0].innerText = "Stop"
        recognizing = true; };

    recognition.onerror = function(event) {
        console.log("Dictate error");
        console.log(event.error);
    };

    recognition.onend = function() {
	$("#start_button")[0].innerText = "Talk"
        recognizing = false;
    };

    recognition.onresult = function(event) {
        console.log(event)
        var interim_transcript = '';
        for (var i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                final_transcript += event.results[i][0].transcript;
            }
        }

        final_transcript = capitalize(final_transcript);

	add_string_in_tags("p", "你: " + final_transcript);

        recognition.stop();

	ask_question(final_transcript)


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

function ask_question(raw_text) {
    $.post( '/foo', {"raw_text" : final_transcript}, function(response) {  
	console.log(response);
        if (response == null) { add_string_in_tags("p", "妹:  我沒聽清楚，請再說一遍") }

        response = JSON.parse(response);


        add_string_in_tags("p", "妹: " + response["dialogueReply"]);

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
        if (url == "None") { return add_string_in_tags("p", " 妹:  查無相關資料"); }
        $( '#schedule_list' ).attr('src', url);
    });
}

function add_string_in_tags(tag_name, content) {
    return $(tag_name).append("<div> " + content + " </div>")
}
