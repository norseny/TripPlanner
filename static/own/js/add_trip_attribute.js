$('document').ready(function(){
    addFormsets()
    $(function () {
        $('input[type=datetime]').datepicker();
    });
});

function addFormsets() {
    const datepickerCallback = function () {
        return function (addedRow) {
            $(addedRow.find('input[type=datetime]')).datepicker();
        }
    };
    $('.formset_row1').formset({
        addText: 'add new row',
        deleteText: 'remove',
        prefix: 'journey_set',
        added: datepickerCallback()
    });
    $('.formset_row2').formset({
        addText: 'add new row',
        deleteText: 'remove',
        prefix: 'accomodation_set',
        added: datepickerCallback()
    });
    $('.formset_row3').formset({
        addText: 'add new row',
        deleteText: 'remove',
        prefix: 'attraction_set',
        added: datepickerCallback()
    });
}