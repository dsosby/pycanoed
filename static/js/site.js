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

    $("#post-timestamp").datepicker();
    $("#post-password").focus();
    
});

function set_canoe_percent(percent)  {
    var max_width = $("header").width();
    var width = Math.min(percent, 1.0) * max_width;
    $("#canoe-progress").width(width + "px");

    if (percent >= 1.0)  {
        $("#fraction-display").hide();
        $("#done-label").show();
    }
}
