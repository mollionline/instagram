function likes(event) {
    event.preventDefault();
    event.stopPropagation();
    let id = event.target.className;
    let count_id = `${id}`;
    $.ajax({
        url: `http://127.0.0.1:8000/api/v1/like/${id}`,
        method: "POST",
        headers: {Authorization: "Token " + localStorage.getItem("apiToken")},
        data: JSON.stringify({post_id: id}),
        dataType: "json",
        contentType: "application/json",
        success: function (response, status) {
            if (response.like == '+') {
                let count = Number($(`#${count_id}`).text()) + 1
                $(`.${count_id}`).attr("src", "/static/images_common/like_red.png");
                $(`#${count_id}`).text(count)
            } else if (response.like == '-') {
                let count = Number($(`#${count_id}`).text()) - 1
                $(`.${count_id}`).attr("src", "/static/images_common/like_white.png");
                $(`#${count_id}`).text(count)
            }
        },
        error: function (response, status) {
            console.log(response.responseJSON.error);
        },
    });
}