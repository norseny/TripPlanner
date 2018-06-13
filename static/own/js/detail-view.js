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
        a = $(this).closest(".truncated-info");
        a.css("cssText", "display: none !important;");
        a.next().slideToggle( "slow");
        var nextel = a.next();
        var iconLess = nextel.find(".icon-show-less");
        iconLess.css("cssText", "display: inline-block !important;");
    });
    $(".icon-show-less").click(function () {
        var a;
        $(this).hide();
        a = $(this).closest(".more-info-to-show");
        $(this).css("cssText", "display: none !important;");
        a.slideToggle( "slow");
        // a.css("cssText", "display: none !important;");
        a.prev().show()
    });
        $("#show-trip-details").click(function () {
        $('#trip-details-table').slideToggle( "slow");
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
        document.getElementById("icon-details-down-view").style.display = "inline-block";
        document.getElementById("icon-details-up-view").style.display = "none";
    } else {
        document.getElementById("icon-details-up-view").style.display = "inline-block";
        document.getElementById("icon-details-down-view").style.display = "none";
    }
    evt.currentTarget.className += " active";
}