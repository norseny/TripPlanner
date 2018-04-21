const params2 = {
    "timePicker": true,
    "timePicker24Hour": true,
    "opens": "center",
    "locale": {
            format: 'DD/MM/YYYY (h:mm)'
        }
};

const params = {
    enableTime: true,
    dateFormat: "d-m-Y H:i",
    locale: language_code,
    time_24hr: true
};

// $('document').ready(function () {
//     addFormsets();
//     $(function () {
//         $('input[type=datetime]').flatpickr(params);
//     });
// });


$('document').ready(function () {
    addFormsets();
    $(function () {
        $('input.datetimepicker-range').daterangepicker(params2);
    });
});


function addFormsets() {
    // const datepickerCallback = function () {
    //     return function (addedRow) {
    //         $(addedRow.find('input[type=datetime]')).flatpickr(params);
    //     }
        const datepickerrangeCallback = function () {
        return function (addedRow) {
            $(addedRow.find('input.datetimepicker-range')).daterangepicker(params2);
        }
    };
    $('.formset_row1').formset({
        addText: '<span class="font-size-bigger">+</span>' + addNewRow,
        deleteText: '<span class="font-size-bigger">-</span>',
        prefix: 'journey_set',
        added: datepickerrangeCallback()
    });

    $('.formset_row2').formset({
        addText: '<span class="font-size-bigger">+</span>' + addNewRow,
        deleteText: '<span class="font-size-bigger">-</span>',
        prefix: 'accommodation_set',
        added: datepickerCallback()
    });

    $('.formset_row3').formset({
        addText: '<span class="font-size-bigger">+</span>' + addNewRow,
        deleteText: '<span class="font-size-bigger">-</span>',
        prefix: 'attraction_set',
        added: datepickerCallback()
    });
}