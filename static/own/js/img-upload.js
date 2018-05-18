$(document).ready(function () {

    var mycheckbox = $("input[type=checkbox]");
    mycheckbox.hide();
    mycheckbox.before(
        "<span class=\"error-style icon-remove mt-2 cursor-pointer\"\n\" + id=\"remove-img-icon\">\n" +
        "<span class=\"fas fa-times-circle\">\n" +
        "</span>"+ removeLbl +"</span>");
    $("label[for=\"main_image-clear_id\"]").hide();

    $("#remove-img-icon").click(function () {
        $(mycheckbox).prop('checked', true);
        var mydiv = mycheckbox.closest("div");
        mydiv.hide();
        mydiv.after(imgRemovedLbl);
    });

    var myfileinput = $("input[type=file]");
    myfileinput.after("<label class=\"btn cursor-pointer\" for=\"id_main_image\">" + selFileLbl + "</label>");
    myfileinput.hide();

    var label = myfileinput.next('label'),
        labelVal = label.html();

    myfileinput.on('change', function (e) {
        var fileName = '';
        if (e.target.value)
            fileName = e.target.value.split('\\').pop();
        if (fileName)
            label.after(fileName);
    });

});