$(document).ready(function () {

    if(($.cookie('id') !== "") && ($.cookie('id') !== "")){
        $("#userFirst").attr("href", "/user/userInfo").html($.parseJSON($.cookie('username')));
        $("#userLast").attr("href", "/user/logout").html("注销");
    }

    $("#goCoop").on("click", function () {
        $(location).attr("href", "/cooperation");
    });

    $("#goProject").on("click", function () {
        $(location).attr("href", "/project");
    });


    $(".tag").on("click", function () {
            $(".allTag").removeClass("active");
            $("#activate").removeClass("active").removeAttr("id");
            $(this).addClass("active");
            $(this).attr("id", "activate");
            if($(".allTag").attr("flag") === "0"){
                urlTag = "projectTag";
            }else {
              urlTag = "cooperationTag"
            }
            $.ajax({
                url: urlTag,
                type: "GET",
                dataType: "json",
                data:"tag="+$("#activate b").html(),
                success: function (msg) {
                    content = $("#allPosts");
                    content.empty();
                    if($.isEmptyObject(msg["posts"])){
                        content.html("<div class='list-group'>没有帖子</div>");
                    }else {
                        $.each(msg["posts"],function (i, n) {
                            content.append('<div class="list-group"><a href="/post/' + n["id"] +
                                '" class="list-group-item"><h3 class="list-group-item-heading">' +
                                n["postTitle"] + '<small>&nbsp;' + n["postTag__tagName"] + '</small></h3>' +
                                '<h6 class="list-group-item-text">' + n["postCreateTime"] + '&nbsp;&nbsp;&nbsp;' +
                                n["postMaster__nickname"] + '</h6><p class="list-group-item-text">' + n["postContent"] +
                                '</p></a></div>');
                        });
                    }
                }
            })
        });

});

