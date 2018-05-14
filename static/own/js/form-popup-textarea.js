$(document).ready(function () {

    moreInfoButtonVisibility();

    $('.button-more-info').click(function () {
        $('#overlay-whole-page').show();
        var divContainer = $(this).closest("div.field");
        var moreInfoTextareaFound = divContainer.children(":first");
        var textAreaInputText = moreInfoTextareaFound.val();
        var timestamp = new Date().getUTCMilliseconds();
        divContainer.append("<div class=\"confirmBox\" style=\"display: none\">\n" +
            "    <textarea id=\"" + timestamp + "\"class=\"materialize-textarea form-control form-control-sm more-info\" rows=\"10\" cols=\"65\"></textarea>\n" +
            "    <div class=\"message\"></div>\n" +
            "    <span class=\"yes btn btn-sm\">Proceed</span>\n" +
            "    <span class=\"no btn btn-sm\">Cancel</span>\n" +
            "</div>"
        );
        $('#' + timestamp).val(textAreaInputText);

    });


});

function doConfirm(msg, yesFn, noFn) {
    var confirmBox = $(".confirmBox");
    confirmBox.find(".message").text(msg);
    confirmBox.find(".yes,.no").unbind().click(function () {
        confirmBox.hide();
    });
    confirmBox.find(".yes").click(yesFn);
    confirmBox.find(".no").click(noFn);
    confirmBox.show();
}

$(function () {
    $("form.textarea-form").submit(function (e) {
        e.preventDefault();
        var form = this;
        doConfirm("Are you sure?", function yes() {
            //form.submit();
            var confirmBox = $(".confirmBox");
            var moreInfoNewTextareaFound = confirmBox.children(":first");
            var textAreaNewInputText = moreInfoNewTextareaFound.val();
            var divContainer = $(this).closest("div.field");
            var moreInfoTextareaFound = divContainer.children(":first");
            moreInfoTextareaFound.val(textAreaNewInputText);
            confirmBox.remove();
            $('#overlay-whole-page').hide();
        }, function no() {
            $(".confirmBox").remove();
            $('#overlay-whole-page').hide();
            // do nothing
        });
    });
});

function moreInfoButtonVisibility() {

    var moreInfoTextarea = $("textarea.more-info");
    moreInfoTextarea.hide();
    moreInfoTextarea.closest(".field").append("" +
        "<form class=\"textarea-form\"method=\"post\" action=\"/#\">\n" +
        "<input type=\"hidden\" name=\"html\" value=\"&lt;p&gt;Your data has been deleted&lt/p&gt;\" />\n" +
        "<button type=\"submit\" class='button-more-info w-100'>\n" +
        "<span class=\"d-block text-center add-more-info-button-icon\">" +
        "<i class=\"fas fa-plus-circle fa-2x\">" +
        "</i></span>\n" +
        "   </button>\n" +
        "</form>");
}
