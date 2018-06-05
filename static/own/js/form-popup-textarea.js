$(document).ready(function () {

    moreInfoButtonVisibility();
});


    $('.add-more-info-button-icon').click(function () {
        $('#overlay-whole-page').show();
        var divContainer = $(this).closest("div.field");
        var moreInfoTextareaFound = divContainer.children(":first");
        var textAreaInputText = moreInfoTextareaFound.val();
        var timestamp = new Date().getUTCMilliseconds();
        divContainer.append("<div class=\"confirmBox\" style=\"display: none\">\n" +
            "    <textarea id=\"" + timestamp + "\"class=\"materialize-textarea form-control form-control-sm more-info\" rows=\"11\" cols=\"65\"></textarea>\n" +
            "    <div class=\"message\"></div>\n" +
            "    <span class=\"no btn btn-sm\">" + cancelText + "</span>\n" +
            "    <span class=\"yes btn btn-sm\">" + saveText + "</span>\n" +
            "</div>");

        $('#' + timestamp).val(textAreaInputText);

        doConfirm("", function yes() {
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


function moreInfoButtonVisibility() {
    var moreInfoTextarea = $("textarea.more-info");
    var nextsib = moreInfoTextarea.next();
    if (moreInfoTextarea.next().length === 0) {
        moreInfoTextarea.hide();
        moreInfoTextarea.closest(".field").append("" +
            "<span class=\"d-block text-center add-more-info-button-icon\">" +
            "<span class=\"fas fa-info fa-2x\"></span><span class=\"fas fa-plus-circle mb-3\">" +
            "</span></span>");
    }
}


function newInfoButtonAndTexarea() {

        moreInfoButtonVisibility();

        $('.add-more-info-button-icon').click(function () {
            $('#overlay-whole-page').show();
            var divContainer = $(this).closest("div.field");
            var moreInfoTextareaFound = divContainer.children(":first");
            var textAreaInputText = moreInfoTextareaFound.val();
            var timestamp = new Date().getUTCMilliseconds();
            divContainer.append("<div class=\"confirmBox\" style=\"display: none\">\n" +
                "    <textarea id=\"" + timestamp + "\"class=\"materialize-textarea form-control form-control-sm more-info\" rows=\"11\" cols=\"65\"></textarea>\n" +
                "    <div class=\"message\"></div>\n" +
                "    <span class=\"no btn btn-sm\">" + cancelText + "</span>\n" +
                "    <span class=\"yes btn btn-sm\">" + saveText + "</span>\n" +
                "</div>");

            $('#' + timestamp).val(textAreaInputText);

            doConfirm("", function yes() {
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
            });


        });
}
