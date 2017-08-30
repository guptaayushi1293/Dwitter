function unFollowUser(followingUserId) {
    var data = {};
    data['followed_to_id'] = followingUserId;
    try {
        $.ajax({
            url: "/dweet/user/unfollow/",
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