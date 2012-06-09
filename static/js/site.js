$(function()  {
    $("#post-password").keyup(function()  {
        $.getJSON("/verify", {password: $("#post-password").val()}, function(result)  {
            if (result.valid)  {
                $("#post-form").show();
                $("#post-title").focus();
            }
        });
    });

    $("#post-password").focus();
});
