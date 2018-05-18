$(document).ready(function () {
    $("#cog-home").click(function () {
        $(this).hide();
        $('#change-lang-home').show();
    });

    $(document).mouseup(function (e) {
        var container = $("#change-lang-home");
        if (!container.is(e.target) && container.has(e.target).length === 0) {
            container.hide();
            $("#cog-home").show();
        }
    });

});
