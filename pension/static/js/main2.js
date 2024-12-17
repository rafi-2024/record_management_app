
$(document).ready(function () {
    // add "Add new" button to the table
    $('[data-toggle="tooltip"]').tooltip();
    var actions = $("table td:last-child").html();
    // Prepend table with add row form on add new button click
    $(".add-new").click(function () {
        $(this).attr("disabled", "disabled");
        var index = $("table tbody tr:last-child").index();
        console.log(index)
        var row = '<tr>' +

            '<td><input type="text" class="form-control" name="refnum" id="refnum"></td>' +
            '<td><input type="date" class="form-control" name="refdate" id="refdate"></td>' +
            '<td><input type="text" class="form-control" name="refsubject" id="refsubject"></td>' +
            '<td><input type="text" class="form-control" name="diaryid" id="diaryid"></td>' +
            '<td>' + actions + '</td>' +
            '</tr>';
        $("table").append(row);
        $("table tbody tr").eq(index).find(".add, .edit, .delete").toggle();
        $('[data-toggle="tooltip"]').tooltip();
    });

    // Add row on add button click
    $(document).on("click", ".add", function (event) {
        console.log("add button clicked")
        var empty = false;
        var input = $('#newrow input').find("td:not(:last-child)");
        console.log("LOGGING INPUT " + input)
        input.each(function () {
            if (!$(this).val()) {
                console.log($(this).val())
                $(this).addClass("error");
                empty = true;
            } else {
                console.log($(this).val())
                $(this).removeClass("error");
            }
        });
        var branchcode = $("#refnum").val();
        var subject = $("#refsubject").val();
        var date = $("#refdate").val();
        var diaryref = $("#diaryid").val();
        
        $.post("/issues/new", { branchcode: branchcode, subject: subject, date: date, diaryref: diaryref }, function (data) {
            console.log(data)
            // $("#displaymessage").html(data);
            // $("#displaymessage").show();
        });

        $(this).parents("tr").find(".error").first().focus();
        if (!empty) {
            input.each(function () {
                $(this).parent("td").html($(this).val());
            });
            $(this).parents("tr").find(".add, .edit").toggle();
            $(".add-new").removeAttr("disabled");
        }
    });

    // Delete row on delete button click
    $(document).on("click", ".delete", function () {
        $(this).parents("tr").remove();
        $(".add-new").removeAttr("disabled");
        var id = $(this).attr("id");
        var string = id;
        console.log(string)
        $.post("/issues/delete", { string: string }, function (data) {
            $("#displaymessage").html(data);
            $("#displaymessage").show();
        });
        // Delete row on delete button click
        $(document).on("click", ".delete", function () {
            $(this).parents("tr").remove();
            $(".add-new").removeAttr("disabled");
            var id = $(this).attr("id");
            var string = id;
            console.log(string)
            $.post("/issues/delete", { string: string }, function (data) {
                // console.log(data)
                // $("#displaymessage").html(data);
                // $("#displaymessage").show();
            });

        });
    });
    // update rec row on edit button click
    $(document).on("click", ".update", function () {
        var id = $(this).attr("id");
        var branchcode = $("#branchcode").val();
        var subject = $("#subject").val();
        var date = $("#date").val();
        var diaryref = $("#diaryref").val();
        $.post("/update/" + id, { id: id, branchcode: branchcode, subject: subject, date: date, diaryref: diaryref }, function (data) {
            $("#displaymessage").html(data);
            $("#displaymessage").show();
            // Redirect to the new page
            // window.location.href = response.redirect_url;

        });


    });
    // Edit row on edit button click
    $(document).on("click", ".edit", function () {
        $(this).parents("tr").find("td:not(:last-child)").each(function (i) {
            if (i == '0') {
                var idname = 'branchcode';
            } else if (i == '1') {
                var idname = 'date';
            } else if (i == '2') {
                var idname = 'subject';
            } else if (i == '3') {
                var idname = 'diaryref';
            } else { }
            $(this).html('<input type="text" name="updaterec" id="' + idname + '" class="form-control" value="' + $(this).text() + '">');
        });
        $(this).parents("tr").find(".add, .edit").toggle();
        $(".add-new").attr("disabled", "disabled");
        $(this).parents("tr").find(".add").removeClass("add").addClass("update");
    });
});
