$(function()  {
    $("#post-password").keyup(function()  {
        $.getJSON("/verify", {password: $("#post-password").val()}, function(result)  {
            if (result.valid)  {
                $("#post-password-field").hide();
                $("#post-form-fields").show();
                $("#post-title").focus();
            }
        });
    });

    $("#post-password").focus();
});
