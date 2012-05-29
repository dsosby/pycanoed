$(function()  {
    $("#post-form").dialog({
        autoOpen: false,
        height:   400,
        width:    600,
        modal:    true,
        buttons:  {
            "Post": function()  {
                alert("Posting");
            },
            Cancel: function()  {
                $(this).dialog("close");
            }
        },
        close: function()  {
                $(this).dialog("close");
        }
    });

    $("#post-button").click(function()  {
        $("#post-form").dialog("open");
    });
})();
