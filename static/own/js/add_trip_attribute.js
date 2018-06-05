const params = {
    dateFormat: "d.m.y",
    locale: language_code,
    time_24hr: true,
    mode: "range",
    minDate: "today"
};

const params2 = {
    enableTime: true,
    dateFormat: "d.m.y (H:i)",
    locale: language_code,
    time_24hr: true
};

$('document').ready(function () {
    addFormsets();
    $(function () {
        $('.daterange').flatpickr(params);
    });
    $(function () {
        $('.datetime').flatpickr(params2);
    });
});


function addFormsets() {

    const datepickerCallback = function () {
        return function (addedRow) {
            $(addedRow.find('.daterange')).flatpickr(params);
            $(addedRow.find('.datetime')).flatpickr(params2);
        }
    };

    $('.formset_row1').formset({
        addText: '<span class="form-plus-minus-js ">+</span>' + addNewRow,
        deleteText: '<span class="form-plus-minus-js">-</span>',
        prefix: 'journey_set',
        added: datepickerCallback(),
        added2: newInfoButtonAndTexarea()

    });

    $('.formset_row2').formset({
        addText: '<span class="form-plus-minus-js">+</span>' + addNewRow,
        deleteText: '<span class="form-plus-minus-js">-</span>',
        prefix: 'accommodation_set',
        added: datepickerCallback(),
        added2: newInfoButtonAndTexarea()

    });

    $('.formset_row3').formset({
        addText: '<span class="form-plus-minus-js">+</span>' + addNewRow,
        deleteText: '<span class="form-plus-minus-js">-</span>',
        prefix: 'attraction_set',
        added: datepickerCallback(),
        added2: newInfoButtonAndTexarea()

    });
}