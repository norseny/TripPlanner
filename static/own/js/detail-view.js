        $(document).ready(function () {
            $('#inspired').click(function () {
                var tripId = {'tripId': trip_id};

                $.ajax({
                    url: '/ajax/inspired/',
                    data: tripId,
                    dataType: 'json',
                    success: function (data) {
                        if (data.error) {
                            alert(data.error)
                        } else {
                            window.location.href = data.tripEditUrl;
                        }
                    }
                });
            });
        });

        function openCloseDetails(evt, id) {
            var myvar;
            myvar = document.getElementById(id);
            if (myvar.style.display == "block") {
                myvar.style.display = "none";
                document.getElementById("icon-details-down-view").style.display = "block";
                document.getElementById("icon-details-up-view").style.display = "none";
            } else {
                myvar.style.display = "block";
                document.getElementById("icon-details-up-view").style.display = "block";
                document.getElementById("icon-details-down-view").style.display = "none";
            }
            evt.currentTarget.className += " active";
        }