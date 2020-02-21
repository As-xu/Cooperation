$(document).ready(function () {
    if(($.cookie('id') !== "") && ($.cookie('id') !== "")){
        $("#userFirst").attr("href", "/user/userInfo").html($.parseJSON($.cookie('id')));
        $("#userLast").attr("href", "/user/logout").html("注销");
    }
});