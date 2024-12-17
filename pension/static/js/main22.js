document.addEventListener('DOMContentLoaded', function () {
    let addNewButton = document.querySelector('.add-new');
        addNewButton.addEventListener('click', function (event) {
            // event.preventDefault()
            let modal = new bootstrap.Modal(document.getElementById('issuemodal'));
            modal.show();
        });
    });