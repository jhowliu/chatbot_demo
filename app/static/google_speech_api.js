var final_transcript = '';
var recognizing = false;

if ('webkitSpeechRecognition' in window) {

    var recognition = new webkitSpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = function() {
	$("#start_button")[0].innerText = "Stop"
        recognizing = true;
    };

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

        $( "p" ).append("<div> 你：" + final_transcript + " </div>");
        // ajax post
        $.post( '/foo', {"raw_text" : final_transcript}, function(response) {  
            response = JSON.parse(response);
            console.log(response);
            //$( ".conversations" ).append("<div> bot  says" + response + "</div>")
            $( "p" ).append("<div> 妹：" + response["dialogueReply"] + " </div>");

            recognition.stop();

            if (response["dialogue_state"] == 'completed') { 
		$.post( '/get_schedule', {"result" : response}, function(response) {
		    console.log(response)
		})
            }

            startDictation(event);

        })
    };
}

var two_line = /\n\n/g;
var one_line = /\n/g;
function linebreak(s) {
    return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
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
