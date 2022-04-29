let loginForm;
loginForm = $('#loginForm')[0];
let username = $('#username')[0];
let password = $('#password')[0];


loginForm.addEventListener('submit', (e) => {
    e.preventDefault();

    $.ajax({
        url: 'http://127.0.0.1:8000/api/v1/login/',
        method: 'post',
        data: JSON.stringify({username: `${username.value}`, password: `${password.value}`}),
        dataType: 'json',
        contentType: 'application/json',
        success: function (response) {
            localStorage.setItem('apiToken', response.token)
        },
        error: function (response) {
            console.log(response);
        }
    });

    loginForm.submit();
})