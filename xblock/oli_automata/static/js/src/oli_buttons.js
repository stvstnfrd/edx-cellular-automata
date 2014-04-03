
$(document).ready(function () {

    $("#oli_automata_save").click(function () {
        $.ajax({
            url: "save_state",
            context: HW.getState()
        });
    });

    $("#oli_automata_grade").click(function () {
        $.ajax({
            url: "grade",
            context: HW.getGrade()
        });
    });

});

