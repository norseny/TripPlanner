$(document).ready(function () {
    $('li.active').removeClass('active');

    $('a[href="' + location.pathname + '"]').closest('li').addClass('active');

    $('.lang').click(function () {
            $('#lang-input').click()
        }
    );
    $('#search-btn').click(function () {
        var searchQuery = $('#input-search').val();
        window.location.href = '/trip/search/' + searchQuery;
    })

});
