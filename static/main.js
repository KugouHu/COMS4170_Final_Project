$(document).ready(function() {
    $('.homeImg').on('error', function() {
        $(this).css('display', 'none');
    });

    $('.learnImg').on('error', function() {
        $(this).attr('alt', 'Image unavailable');
        $(this).css({
            'background': '#f0f0f0',
            'height': '220px'
        });
    });

    $('.quizImg').on('error', function() {
        $(this).attr('alt', 'Image unavailable');
    });
});