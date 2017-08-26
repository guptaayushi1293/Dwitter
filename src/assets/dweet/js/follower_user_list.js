$(document).ready(function() {
    if($(".follow_btn").length) {
        $(".follow_btn").click(function() {
            var buttonId = this.id;
            var followUserId = parseInt(buttonId.replace("follow_", ""));
            followUser(followUserId);
        });
    }
});

function followUser(followUserId) {
    var data = {};
    data['followed_to_id'] = followUserId;
    try {
        $.ajax({
            url: "/dweet/user/follow/",
            type: "POST",
            async: false,
            data: {
                data: JSON.stringify(data)
            },
            success: function(response) {
                if(response['statusCode'] == 0) {
                    alert(response['statusMessage']);
                    location.reload(true);
                }
                else {
                    alert(response['statusMessage']);
                }
            },
            error: function() {
                console.log("Error.");
            }
        });
    }
    catch(ex) {
        console.log("Exception occurred while performing this action : " + ex.toString());
    }
}