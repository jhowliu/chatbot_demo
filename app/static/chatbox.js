var Chatbox = {
    show_chatbox: function() {
        console.log("show chatbox")
        $(".chatbox").addClass('active');
        $(".chatbox-exit").addClass('active');
    },

    close_chatbox: function() {
        console.log("close chatbox")
        $(".chatbox").removeClass('active')
        $(".chatbox-exit").removeClass('active');
    },

    load: function() {
        $(".chatbox-btn").on("click", Chatbox.show_chatbox)
        $(".chatbox-exit").on("click", Chatbox.close_chatbox) 
    }
}

$(document).ready(function () {
    Chatbox.load();
});
