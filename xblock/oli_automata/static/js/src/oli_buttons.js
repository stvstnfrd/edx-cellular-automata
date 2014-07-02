function OLIAutomataXBlock(runtime, element) {
    $("#oli_automata_save").click(function (eventObject) {
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'save_state'),
            data: HW.getState()
        });
    });

    $("#oli_automata_grade").click(function (eventObject) {
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'grade'),
            data: HW.getGrade(),
            success: function (data) {
                if (data.completed && !data.errors) {
                    console.log('grade', data));
                }
            },
        });
    });

    $(function ($) {
        $.ajax({
            url: runtime.handlerUrl(element, 'load_state'),
            success: function (data) {
                console.log("load_state", data)
                HW.setState(0, data);
            }
        });
    });
}

