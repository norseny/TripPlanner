$(document).ready(function () {
    $("#journey-acc").click(function () {
        if ($('#icon-up-journey').is(':visible')) {
            $("#icon-up-journey").hide();
            $("#icon-down-journey").show();
        } else {
            $("#icon-up-journey").show();
            $("#icon-down-journey").hide();

        }
    });
    $("#accommodation-acc").click(function () {
        if ($('#icon-down-accommodation').is(':visible')) {
            $("#icon-down-accommodation").hide();
            $("#icon-up-accommodation").show();
        } else {
            $("#icon-down-accommodation").show();
            $("#icon-up-accommodation").hide();
        }
    });
    $("#attraction-acc").click(function () {
        if ($('#icon-down-attraction').is(':visible')) {
            $("#icon-down-attraction").hide();
            $("#icon-up-attraction").show();
        } else {
            $("#icon-down-attraction").show();
            $("#icon-up-attraction").hide();
        }
    });
});