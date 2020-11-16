
// start variables

document.addEventListener('DOMContentLoaded', function() {

    // start variables

    // load functions

});


function lop_new_toggle() {
    $('#lop_new').toggle();    
}


function lop_new() {

    // start variables
    const csrftoken = getCookie('csrftoken');
    const project = $('#lop_newname').val();
    
    // fetch url
    fetch(`/api_user`, {
        method: 'POST',
        mode: 'same-origin',  // Do not send CSRF token to another domain.
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            project: project
        })
    })
    .then(response => response.json())
    .then(result => {

        // Print result
        console.log(result);

        if (result.error) {
            alert(result.error);            
        } else if (result.message) {
            alert(result.message);
        }
    }) 
}