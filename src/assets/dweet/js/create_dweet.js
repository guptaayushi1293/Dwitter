$(document).ready(function() {
    if($("#create_dweet").length) {
        $("#create_dweet").click(function() {
            var content = document.getElementById("dweet_content").value;
            if(content == "" || content == undefined) {
                alert("Tweet content cannot be empty.");
                return;
            }
            else {
                //post ajax request
                addDweet(content);
            }
        });
    }
});

function addDweet(content) {
    var data = {};
    data['content'] = content;
    console.log(data);
    try {
        $.ajax({
            url: "/dweet/add/",
            type: "POST",
            async: false,
            data: {
                "data": JSON.stringify(data)
            },
            success: function(response) {
                if(response['statusCode'] == 0) {
                    alert(response['statusMessage']);
                    location.reload(true);
                }
                else {
                    alert(response['statusMessage']);
                    return;
                }
            },
            error: function() {
                console.log("Error");
                return;
            }
        });
    }
    catch(ex) {
        console.log("Exception occurred while adding dweet : " + ex.toString());
    }
}