const params = {
    enableTime: true,
    dateFormat: "d-m-Y H:i",
    locale: language_code,
    time_24hr: true
};

$('document').ready(function () {
    addFormsets();
    $(function () {
        $('input[type=datetime]').flatpickr(params);
    });
});

function addFormsets() {
    const datepickerCallback = function () {
        return function (addedRow) {
            $(addedRow.find('input[type=datetime]')).flatpickr(params);
        }
    };
    $('.formset_row1').formset({
        addText: '<span class="font-size-bigger">+</span> Add new row', //todo: tłumaczenie - trans nie dziala
        deleteText: '<span class="font-size-bigger">-</span>',
        prefix: 'journey_set',
        added: datepickerCallback()
    });

    $('.formset_row2').formset({
        addText: '<span class="font-size-bigger">+</span>',
        deleteText: '<span class="font-size-bigger">-</span>',
        prefix: 'accommodation_set',
        added: datepickerCallback()
    });

    $('.formset_row3').formset({
        addText: '<span class="font-size-bigger">+</span>',
        deleteText: '<span class="font-size-bigger">-</span>',
        prefix: 'attraction_set',
        added: datepickerCallback()
    });
}