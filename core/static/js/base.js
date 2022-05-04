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
        let template = [
            '<div class="row fs-3 task"><span class="e-name col-10" data-bs-toggle="collapse" data-bs-target=".desc[data-id=\'',
            '\']"aria-expanded="false" aria-controls="collapseExample">',
            '<span class="badge bg-primary">',
            '</span></h1></span><div class="e-actions col-2 d-flex align-items-center justify-content-center"><i class="fa-solid fa-check"></i>' + 
            '<i class="fa-solid fa-xmark"></i></div><div class="col-10 collapse fs-5 desc" data-id="',
            '"><p>Przewidywana data wykoniania: ',
            '</p>',
            '</div></div>'

        ]
        let newTasksContainer = $('#t-new');
        let doneTasksContainer = $('#t-done');

        newTasksContainer.empty();
        doneTasksContainer.empty();

        data.forEach(e => {
            let category;
            let html = ''
            if (e['category'] === 1) {
                category = 'FrontEnd'
            } else {
                category = 'BackEnd'
            }
            html += template[0];
            html += e['id'];
            html += template[1];
            html += e['name'];
            html += template[2];
            html += category;
            html += template[3];
            html += e['id'];
            html += template[4];
            html += e['prediction'];
            html += template[5];
            html += e['description'];
            html += template[6];
            
            if (e['status'] == 1) {
                newTasksContainer.append(html);
            } else {
                doneTasksContainer.append(html);
            }
        });
    }

});