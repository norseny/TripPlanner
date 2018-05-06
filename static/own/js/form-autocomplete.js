$(document).on('focus', '.autocomplete', function () {
    $("#" + document.activeElement.id).autocomplete({
        source: "/autocomplete/get_places/",
        select: function (event, ui) { //item selected
            AutoCompleteSelectHandler(event, ui)
        },
        minLength: 2
    });
});

function AutoCompleteSelectHandler(event, ui) {
    var selectedObj = ui.item;
}
