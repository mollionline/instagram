let logoutBtn = $('#logoutBtn')[0];


logoutBtn.addEventListener('click', () => {
    $.ajax({
        url: 'http://127.0.0.1:8000/api/v1/logout/',
        method: 'post',
        headers: {'Authorization': 'Token ' + `${localStorage.apiToken}`},
        dataType: 'json',
        success: function (response) {
            localStorage.removeItem('apiToken');
        },
        error: function (response) {
            console.log(response);
        }
    });
})