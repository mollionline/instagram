function likes(e) {
    e.preventDefault();
    let post = $("#post_id").val();
    $.ajax({
        url: `http://127.0.0.1:8000/api/v1/like/${post}`,
        method: "POST",
        headers: {Authorization: "Token " + localStorage.getItem("apiToken")},
        data: JSON.stringify({post_id: post}),
        dataType: "json",
        contentType: "application/json",
        success: function (response, status) {
            if (response.like == '+') {
                let count = Number($('#count').text()) + 1
                $("#like_icon").attr("src", "/static/images_common/like_red.png");
                $('#count').html(count)
            } else if (response.like == '-') {
                let count = Number($('#count').text()) - 1
                $("#like_icon").attr("src", "/static/images_common/like_white.png");
                $('#count').html(count)
            }
            console.log(response)
        },
        error: function (response, status) {
            console.log(response.responseJSON.error);
        },
    });
}
$("#post_id").click(likes);