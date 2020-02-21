
$(document).ready(function () {

    $('#myModal').on("show.bs.modal", function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var recipient = button.data("whatever"); // Extract info from data-* attributes
    var modal = $(this);
    modal.find(".control-label").text("请输入" + recipient);
    });

    $("#innerPosts").css("display", "block");

});







