var Utils = {
    format_date: function (format) {
        date = new Date()

        var y = date.getFullYear()
        var m = date.getMonth() + 1;
        var d = date.getDate();
        var h = date.getHours();
        var n = date.getMinutes();
        var s = date.getSeconds();
        var w = date.getDay();

        return format.replace("yyyy", y).replace("yy", y % 100 < 10 ? "0" + y % 100 : y % 100)
                     .replace("MM", m < 10 ? "0" + m : m).replace("M", m)
                     .replace("dd", d < 10 ? "0" + d : d).replace("d", d)
                     .replace("HH", h < 10 ? "0" + h : h).replace("H", h)
                     .replace("mm", n < 10 ? "0" + n : n).replace("m", n)
                     .replace("ss", s < 10 ? "0" + s : s).replace("s", s);
    },

    escape_html: function (s) {
        if (s == null) {
            return "";
        }

        if (typeof (s) != "string") {
            s = s + "";
        }

        return s.replace(/&/g, "&amp;")
                .replace(/\>/g, "&gt;")
                .replace(/\</g, "&lt;")
                .replace(/\'/g, "&#39;")
                .replace(/\"/g, "&quot;")
                .replace(/\n/g, "<br>");
    }
}
