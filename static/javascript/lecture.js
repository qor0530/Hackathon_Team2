document.addEventListener('DOMContentLoaded', function() {
    var element = document.getElementById('go-to-subject-select');
    if (element) {
        element.addEventListener('click', function() {
            window.location.href = '/lecture/subject';
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var element = document.getElementById('go-to-study-write');
    if (element) {
        element.addEventListener('click', function() {
            window.location.href = '/lecture/write/1';
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var element = document.getElementById('go-to-study-situation');
    if (element) {
        element.addEventListener('click', function() {
            window.location.href = '/lecture/situation/1';
        });
    }
});