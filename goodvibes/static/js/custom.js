var controller = (function () {
    var index = 0, data = [];

    function load() {
        var filename = 'static/flash/' + encodeURI(data[index]);
        document.getElementsByName("movie")[0].setAttribute('value', filename);
        document.getElementById("flash").setAttribute('data', filename);
        location.hash = encodeURI(data[index]);
    }

    return {
        init: function (videos) {
            data = videos;
        },
        inc: function () {
            index = (index >= data.length - 1) ? 0 : index + 1;
            load();
        },
        dec: function () {
            index = (index <= 0) ? data.length - 1 : index - 1;
            load();
        },
        rand: function () {
            var min = 0;
            var max = data.length;
            index = Math.floor(Math.random() * (max - min)) + min;
            load();
        },
        select: function () {
            var n = data.indexOf(document.getElementById("search-box").value);
            if (n == -1) return;
            index = n;
            load();
        }
    }
})();


function checkKey(e) {
    e = e || window.event;
    if (e.keyCode == '37') {
        // left arrow
        controller.dec();
    }
    else if (e.keyCode == '39') {
        // right arrow
        controller.inc();
    }
    else if (e.keyCode == '0' || e.keyCode == '32') {
        // space
        controller.rand();
    }
}
document.onkeydown = checkKey;


window.onload = function () {
    controller.init(videos);
    controller.rand();
};