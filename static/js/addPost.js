$(document).ready(function () {
    $("InputTag").remove();
    var state = 1;
    $.ajax({
        type: "GET",
        url: "/getTag",
        dataType: "JSON",
        data: {},
        success: function (msg) {
            // $("#InputTag").prepend("<option value='0'>请选择</option>");
            for(var i in msg){
                $("#InputTag").prepend("<option value='"+i+"'>"+msg[i]+"</option>");
            }
        }
    });
    // $("#name").html($.parseJSON($.cookie("username")));
});