$(document).ready(function () {
    var host = $(location).attr('host'); 
    var employee = $('#employee').data('id');
    var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');

    function getTasks() {
        $.ajax({
            url: '/api/tasks',
            data: {
                employee: employee,
                sort: 'status'
            },
            success: (data) => {
                displayTasks(data);
                setupEventListeners();
            },
        });
    }

    function displayTasks(data) {
        let template = [
            '<div class="row fs-3 task"><span class="e-name col-10" data-bs-toggle="collapse" data-bs-target=".desc[data-id=\'',
            '\']"aria-expanded="false" aria-controls="collapseExample">',
            '<span class="badge bg-primary">',
            '</span></h1></span><div class="e-actions col-2 d-flex align-items-center justify-content-center">',
            '<i class="fa-solid fa-check fs-2 e-check" data-id="',
            '"></i>',
            '<i class="fa-solid fa-xmark fs-2 e-delete" data-id="',
            '"></i></div><div class="col-10 collapse fs-5 desc" data-id="',
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
            let container;
            let html = ''
            if (e['category'] === 1) 
                category = 'FrontEnd'
            else 
                category = 'BackEnd'
             
            html += template[0];
            html += e['id'];
            html += template[1];
            html += e['name'];
            html += template[2];
            html += category;
            html += template[3];
            if (e['status'] == 1) {
                container = newTasksContainer;
                html += template[4];
                html += e['id'];
                html += template[5];
            } else {
                container = doneTasksContainer;
            }
            
            html += template[6];
            html += e['id'];
            html += template[7];
            html += e['prediction'];
            html += template[8];
            html += e['description'];
            container.append(html);
        });
    }

    function setupEventListeners() {
        // TODO: remove set timeout
        $('.e-check').click( e => {
            $.ajax({
                url: '/api/task/' + $(e.target).attr('data-id'),
                type: "PATCH",
                data: {'status': 2},
                success: setTimeout(() => { getTasks(); }, 1000)
            });
        })
        $('.e-delete').click(e => {
            $.ajax({
                url: '/api/task/' + $(e.target).attr('data-id'),
                type: "DELETE",
                headers: { "X-CSRFToken": $crf_token },
                success: setTimeout(() => { getTasks(); }, 1000)
            });
        })
    }

    getTasks();

});