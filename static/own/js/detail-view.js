$(document).ready(function () {
    $('#inspired').click(function () {
        var tripId = {'tripId': trip_id};

        $.ajax({
            url: '/ajax/inspired/',
            data: tripId,
            dataType: 'json',
            success: function (data) {
                if (data.error) {
                    alert(data.error)
                } else {
                    window.location.href = data.tripEditUrl;
                }
            }
        });
    });
    $(".icon-show-more").click(function () {
        var a;
        a = $(this).closest("div.d-flex");
        a.next().show();
        a.css("cssText", "display: none !important;");
    });
    $(".icon-show-less").click(function () {
        var a;
        a = $(this).closest("div.more-info-to-show");
        a.prev().show();
        a.hide()
    });
    $('#add-to-fav-btn').click(function () {
        var tripId = {'tripId': trip_id};

        $.ajax({
            url: '/ajax/add-to-fav/',
            data: tripId,
            dataType: 'json',
            success: function (data) {
                if (data.success==true) {
                    location.reload();
                }else if (data.error) {
                    alert(data.error)
                }
            }
        });
    });

});

function openCloseDetails(evt, id) {
    var myvar;
    myvar = document.getElementById(id);
    if (myvar.style.display == "block") {
        myvar.style.display = "none";
        document.getElementById("icon-details-down-view").style.display = "block";
        document.getElementById("icon-details-up-view").style.display = "none";
    } else {
        myvar.style.display = "block";
        document.getElementById("icon-details-up-view").style.display = "block";
        document.getElementById("icon-details-down-view").style.display = "none";
    }
    evt.currentTarget.className += " active";
}

// $( "#trip-details" ).click(function() {
//   $( "#trip-details-table" ).slideToggle( "slow", function() {
//     // Animation complete.
//   });
// });