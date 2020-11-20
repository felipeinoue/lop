
// start variables
let Fproject_id = 0;
let Frole_dict = [];
let Fusername = '';
let Femail = '';

document.addEventListener('DOMContentLoaded', function() {

    // start variables

    // load functions

    // load lop lists
    load_lop_lists();
    load_roles();

});


function load_roles() {
    // start variables

    // fetch
    fetch(`/api_roles`)
    .then(response => response.json())
    .then(result => {

        // get all roles and transfer to global variable
        Frole_dict = result;

    })   
}


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


function load_view(view) {

    // hide all views
    document.getElementById('startscreen_view').style.display = 'none';    
    document.getElementById('project_view').style.display = 'none';    
    document.getElementById('members_view').style.display = 'none';    
    document.getElementById('profile_view').style.display = 'none';    

    // show selected view
    document.getElementById(view).style.display = 'block';    

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

    // load members table
    load_members_table()

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

        // reload members table
        load_members_table()
    }) 
}


function load_members_table() {
    // start variables

    // fetch
    fetch(`/api_members_table/${Fproject_id}`)
    .then(response => response.json())
    .then(result => {

        // clean up table body
        $("#members_table_body").empty();

        result.forEach(members => {

            // create elements

            // row
            const tr = document.createElement('tr');
            tr.id = `${members.user_id}_members_table_row`

            // username
            const td_username = document.createElement('td');
            td_username.style.border = '1px solid';
            td_username.innerHTML = `${members.username}`;

            // email
            const td_email = document.createElement('td');
            td_email.style.border = '1px solid';
            td_email.innerHTML = `${members.email}`;

            // role
            const td_role = document.createElement('td');
            td_role.style.border = '1px solid';

                // select
                const role_select = document.createElement('select');
                role_select.id = `${members.user_id}_members_role_select`
                role_select.setAttribute('onchange', 'members_role_update(event)')

                // append
                td_role.append(role_select);

                // option
                for (let index = 1; index < (Object.keys(Frole_dict).length + 1); index++) {
                    const role_option = document.createElement('option');
                    role_option.value = index;
                    role_option.innerHTML = Frole_dict[`${index}`];
                    if (members.role_id === index) {
                        role_option.setAttribute('selected', 'selected');
                    }

                    // append
                    role_select.append(role_option);
                }

            // weekly email
            const td_weeklyemail = document.createElement('td');
            td_weeklyemail.style.border = '1px solid';

                // input
                const weeklyemail_input = document.createElement('input');
                weeklyemail_input.id = `${members.user_id}_members_weeklyemail_input`
                weeklyemail_input.type = 'checkbox';
                weeklyemail_input.setAttribute('onchange', 'members_weeklyemail_update(event)')
                if (members.weeklyemail) {
                    weeklyemail_input.setAttribute('checked', 'checked');
                }

                // append
                td_weeklyemail.append(weeklyemail_input);

            // manage
            const td_manage = document.createElement('td');
            td_manage.style.border = '1px solid';

                // a
                const remove_a = document.createElement('a');
                remove_a.id = `${members.user_id}_members_remove_a`;
                remove_a.href = '#';
                remove_a.setAttribute('onclick', 'members_remove_a(event)')
                remove_a.innerHTML = 'remove';

                // append
                td_manage.append(remove_a);

            // append to table row
            tr.append(td_username);
            tr.append(td_email);
            tr.append(td_role);
            tr.append(td_weeklyemail);
            tr.append(td_manage);

            // append to the page
            document.getElementById('members_table_body').append(tr);

        });
    })   
}


function members_role_update(event) {

    // get element that triggered the event
    const element = event.target;

    // start variables
    const csrftoken = getCookie('csrftoken');
    const user_id = element.id.replace('_members_role_select', '');
    const role_id = element.value;
    
    // freeze screen
    $('#myModal').toggle();

    // fetch url
    fetch(`/api_members_table/${Fproject_id}`, {
        method: 'POST',
        mode: 'same-origin',  // Do not send CSRF token to another domain.
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            user_id: user_id,
            role_id: role_id
        })
    })
    .then(response => response.json())
    .then(result => {

        // get options from select
        const options = element.children;

        // update select attribute from role id
        for (const option of options) {
            option.setAttribute('selected', '');
            if (option.value == result['role_id']) {
                option.setAttribute('selected', 'selected')
            }
        }

        // unfreeze screen
        $('#myModal').toggle();

    }) 
}


function members_weeklyemail_update(event) {

    // get element that triggered the event
    const element = event.target;

    // start variables
    const csrftoken = getCookie('csrftoken');
    const user_id = element.id.replace('_members_weeklyemail_input', '');
    const weeklyemail = element.checked;
    
    // freeze screen
    $('#myModal').toggle();

    // fetch url
    fetch(`/api_members_table/${Fproject_id}`, {
        method: 'POST',
        mode: 'same-origin',  // Do not send CSRF token to another domain.
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            user_id: user_id,
            weeklyemail: weeklyemail
        })
    })
    .then(response => response.json())
    .then(result => {

        // update checkbox
        element.checked = result['weeklyemail'];

        // unfreeze screen
        $('#myModal').toggle();

    }) 
}


function members_remove_a(event) {

    // get element that triggered the event
    const element = event.target;

    // start variables
    const csrftoken = getCookie('csrftoken');
    const user_id = element.id.replace('_members_remove_a', '');
    
    // freeze screen
    $('#myModal').toggle();

    // fetch url
    fetch(`/api_members_table/${Fproject_id}`, {
        method: 'POST',
        mode: 'same-origin',  // Do not send CSRF token to another domain.
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            user_id: user_id,
            remove: 'remove'
        })
    })
    .then(response => response.json())
    .then(result => {

        // user removed succesfully
        if (result.message) {

            // remove user row
            $(`#${user_id}_members_table_row`).remove()
        } else {

            // user not removed for some reason
            alert('There was a problem removing this user. Contact the administrator.')
        }

        // unfreeze screen
        $('#myModal').toggle();

    }) 
}


function load_profile() {

    load_view('profile_view');
    
}


function profile_username_save() {

    // start variables
    const csrftoken = getCookie('csrftoken');
    const username = document.getElementById('profile_username').value;

    // fetch url
    fetch(`/api_profile_username_save`, {
        method: 'POST',
        mode: 'same-origin',  // Do not send CSRF token to another domain.
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            username: username
        })
    })
    .then(response => response.json())
    .then(result => {

        // Print result
        console.log(result);

        // display result
        if (result.error) {

            // error
            alert(result.error)

        } else if(result.message) {
          
            // success, reload page
            location.reload();

        }
    }) 
}


function profile_email_save() {

    // start variables
    const csrftoken = getCookie('csrftoken');
    const email = document.getElementById('profile_email').value;

    // fetch url
    fetch(`/api_profile_email_save`, {
        method: 'POST',
        mode: 'same-origin',  // Do not send CSRF token to another domain.
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            email: email
        })
    })
    .then(response => response.json())
    .then(result => {

        // Print result
        console.log(result);

        // display result
        if (result.error) {

            // error
            alert(result.error)

        } else if(result.message) {
          
            // success, reload page
            location.reload();

        }
    }) 
}


function profile_password_save() {

    // start variables
    const csrftoken = getCookie('csrftoken');
    const password = document.getElementById('profile_password').value;
    const confirmation = document.getElementById('profile_confirmation').value;

    // fetch url
    fetch(`/api_profile_password_save`, {
        method: 'POST',
        mode: 'same-origin',  // Do not send CSRF token to another domain.
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            password: password,
            confirmation: confirmation
        })
    })
    .then(response => response.json())
    .then(result => {

        // Print result
        console.log(result);

        // display result
        if (result.error) {

            // error
            alert(result.error)

        } else if(result.message) {
          
            // success, reload page
            location.reload();

        }
    }) 
}
