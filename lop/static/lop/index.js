
// start variables
let Fproject_id = 0;

document.addEventListener('DOMContentLoaded', function() {

    // start variables

    // load functions

    // load lop lists
    load_lop_lists();

});

function load_lop_lists() {
    // start variables

    // fetch
    fetch(`/api_lops`)
    .then(response => response.json())
    .then(result => {
        result.forEach(lop_list => {

            // check if element already exists
            const xls = document.getElementById('lop_lists').childNodes;

            let xskip = false;

            for (let index = 0; index < xls.length; index++) {
                try {
                    const xid = xls[index].id.replace('lop_list_project_id_', '');
                    if (xid == lop_list.project_id) {
                        xskip = true;
                    }                        
                } catch (error) {
                    // 
                }
            }

            // if element doesnt exist, create and append
            if (!xskip) {

                // create element
                const a = document.createElement('a');
                a.id = `lop_list_project_id_${lop_list.project_id}`;
                a.href = '#project';
                a.className = 'w3-bar-item w3-button w3-padding';
                a.addEventListener('click', function() {load_lop_details(lop_list.project_id)});
                a.innerHTML = `${lop_list.project}`;

                // append to the page
                document.getElementById('lop_lists').append(a);
            }
        });
    })   
}


function load_view(view_id) {

    // hide all views
    document.getElementById('startscreen_view').style.display = 'none';    
    document.getElementById('project_view').style.display = 'none';    
    document.getElementById('members_view').style.display = 'none';    

    // show selected view
    document.getElementById(view_id).style.display = 'block';    

}


function lop_new_toggle() {
    $('#lop_new').toggle();    
}


function lop_new() {

    // start variables
    const csrftoken = getCookie('csrftoken');
    const project = $('#lop_newname').val();
    
    // fetch url
    fetch(`/api_lops`, {
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

            // clean up input text
            document.getElementById('lop_newname').value = '';

            // reload lop lists
            load_lop_lists();
        }
    }) 
}


function load_lop_details(project_id) {

    // start variables
    Fproject_id = project_id

    // fetch
    fetch(`/api_lop_details/${project_id}`)
    .then(response => response.json())
    .then(result => {

        // load lop name
        document.getElementById('header_project_name').innerHTML = result['project'];

        // load view
        load_view('project_view');

    })
}


function load_members() {
    
    // prepare page
    document.getElementById('members_textarea').value = '';

    // load view
    load_view('members_view');

}


function members_add() {

    // start variables
    const csrftoken = getCookie('csrftoken');

    // get emails from textarea and transform in list
    const emails = document.getElementById('members_textarea').value.split('\n');

    // fetch url
    fetch(`/api_members_add`, {
        method: 'POST',
        mode: 'same-origin',  // Do not send CSRF token to another domain.
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            project_id: Fproject_id,
            emails: emails
        })
    })
    .then(response => response.json())
    .then(result => {

        // Print result
        console.log(result);

        alert(`added emails: ${result['emails_added']}\ninvalid emails: ${result['emails_invalid']}`)

        // // clean up input text
        document.getElementById('members_textarea').value = '';

        // // reload lop lists
        // load_lop_lists();
    }) 
}
