var myinput = '';

$(document).ready(function () {
    $(".verify-new-participant").click(function () {
        var form = $('.md-form');
        var tripId = {'tripId': trip_id};

        data = form.serialize() + '&' + $.param(tripId);

        $.ajax({
            url: '/ajax/validate-participant',
            data: data,
            dataType: 'json',
            success: function (data) {
                $('#check_icon').show();
                $('#check_icon').css('visibility', 'visible');
                $('#check_icon').css('font-style', 'italic');
                if (data.exists) {
                    $('#check_icon').css('color', '#4caf50');
                    $('#check_icon').html("<span class='fas fa-check fa-2x green-text' aria-hidden='true'><\/span>" +
                        data.message_text);
                    $('#add-button').show();
                    $('.verify-new-participant').hide()
                    myinput = $('.new-participant');
                }
                else {
                    $('#check_icon').css('color', '#bf0000');
                    $('#check_icon').html("<span class='fas fa-times fa-2x' aria-hidden='true'><\/span>" + data
                        .message_error);
                    myinput = $('.new-participant');
                }
            }
        });
    });

    $("#add-button").click(function () {
        var form = $('.md-form');
        var tripId = {'tripId': trip_id};

        data = form.serialize() + '&' + $.param(tripId);

        $.ajax({
            url: '/ajax/add-participant',
            data: data,
            dataType: 'json',
            success: function (data) {
                if (data.success == true) {
                    location.reload();
                }
            }
        });
    });

    $(".new-participant").on("change keyup", function () {
        $('.verify-new-participant').show();
        if ($(this).val() != myinput) {
            $("#add-button").hide();
            $('#check_icon').hide();
        }
    });

});

function removeParticipant(userId) {
    $.ajax({
        url: '/ajax/remove-participant',
        data: "userId=" + userId + "&tripId=" + trip_id,
        dataType: 'json',
        success: function (data) {
            if (data.success == true) {
                location.reload();
            }
        }
    });
}