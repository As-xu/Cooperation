$(document).ready(function () {
    var attr = "";
    $('#myModal').on("show.bs.modal", function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var recipient = button.data("whatever"); // Extract info from data-* attributes
    var modal = $(this);
    attr = button.data("attr");
    modal.find(".control-label").text("请输入" + recipient);
    });

    $("#innerPosts").css("display", "block");
    // $("#userFirst").html($.parseJSON($.cookie("username")));

    $("#data-set").on("click", function () {
        $.ajax({
            url: "infoSet",
            type: "get",
            data: "attr="+attr+"&value="+$("#message-text").val(),
            dataType: "json",
            success: function (msg) {
                $("#"+attr+" b").html(msg[attr]);
                alert("修改成功");
            },
        })
    })

});
