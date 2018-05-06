
const params = {
     enableTime: true,
     dateFormat: "d/m/Y (H:i)",
     locale: language_code,
     time_24hr: true
 };
//
// const paramst = {
//     plugins: rangePlugin({ input: ".secondRangeInput"}),
//     enableTime: true,
//     mode: "range",
//     minDate: "today",
//     dateFormat: "d/m/Y (H:i)",
//     locale: language_code,
//     time_24hr: true
// };

// const params2 = {
//     "timePicker": true,
//     "timePicker24Hour": true,
//     "opens": "center",
//     "locale": {
//             format: 'DD/MM/YYYY (h:mm)' //language_code??
//         }
// };

$('document').ready(function () {
    addFormsets();
    $(function () {
        $('input[type=datetime]').flatpickr(params);
    });
});

function addFormsets() {
        // const datepickerrangeCallback = function () {
        //     return function (addedRow) {
        //         $(addedRow.find('input.datetimepicker-range')).daterangepicker(params2);
        //         }
        //     };
        const datepickerCallback = function () {
            return function (addedRow) {
                $(addedRow.find('input[type=datetime]')).flatpickr(params);
            }
        };

        $('.formset_row1').formset({
        addText: '<span class="font-size-bigger ">+</span>' + addNewRow,
        deleteText: '<span class="font-size-bigger">-</span>',
        prefix: 'journey_set',
        added: datepickerCallback()
    });

    $('.formset_row2').formset({
        addText: '<span class="font-size-bigger">+</span>' + addNewRow,
        deleteText: '<span class="font-size-bigger">-</span>',
        prefix: 'accommodation_set',
        added: datepickerCallback(),
    });

    $('.formset_row3').formset({
        addText: '<span class="font-size-bigger">+</span>' + addNewRow,
        deleteText: '<span class="font-size-bigger">-</span>',
        prefix: 'attraction_set',
        added: datepickerCallback()
    });
}