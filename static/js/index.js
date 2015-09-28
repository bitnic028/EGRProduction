/**
 * Created by antondementyev on 24.09.15.
 */

$(document).ready(function(){

});

function get_object() {
    $.ajax({
        type: "POST",
        url: "/get_object/",
        data:{
            "object_type": $("#objectType").val(),
            "object_id": $("#objectId").val(),
            "_xsrf": getCookie("_xsrf")
        },
        success: function(data) {
            if (data["result"]) {
                $("#placeholder").text(data["data"]);
                //console.log(data["data"]);
            }
            else {
                $("#error-block").text(data["reason"]);
            }
        }
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}