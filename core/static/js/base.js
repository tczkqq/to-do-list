$(document).ready(function () {
    var host = $(location).attr('host'); 
    var employee = $('#employee').data('id');
    $.ajax({
        url: '/api/tasks',
        data: {
            employee: employee,
            sort: 'status'
        },
        success: (data) => {
            displayTasks(data);
        },
    });

    function displayTasks(data) {
        let newTasksContainer = $('#new');
        let doneTasksContainer = $('#done');
        data.forEach(e => {
            if (e['status'] == 1) {
                console.log("New task");
            } else {
                console.log("Done Task");
            }
        });
    }

});