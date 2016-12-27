function selectFlash() {
    var flash = document.getElementById('search-box').value;
    var href = window.location.protocol + '//' + window.location.host + '/' + encodeURIComponent(flash);
    window.location.replace(href);
    return false;
}

function checkKey(e) {
    e = e || window.event;
    if (e.keyCode == '37') {
        // left arrow
        document.getElementById('prev-button').click();
    }
    else if (e.keyCode == '39') {
        // right arrow
        document.getElementById('next-button').click();
    }
    else if (e.keyCode == '0' || e.keyCode == '32') {
        // space
        var href = window.location.protocol + '//' + window.location.host;
        window.location.replace(href);
    }
}
document.onkeydown = checkKey;