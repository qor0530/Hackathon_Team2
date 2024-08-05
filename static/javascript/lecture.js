document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    var element = document.getElementById('go-to-subject-select');
    if (element) {
        console.log('Element found');
        element.addEventListener('click', function() {
            console.log('Element clicked');
            window.location.href = 'subjectSelect.html';
        });
    } else {
        console.log('Element not found');
    }
});
