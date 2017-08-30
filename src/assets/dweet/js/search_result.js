$(document).ready(function () {
    if($(".unfollow-btn").length) {
        $(".unfollow-btn").click(function() {
            var id = this.id;
            var userId = parseInt(id.replace("unfollow_", ""));
            if(isNaN(userId)) {
                alert("Cannot perform this action.");
                return;
            }
            unFollowUser(userId);
        });
    }

    if($(".follow-btn").length) {
        $(".follow-btn").click(function() {
            var id = this.id;
            var userId = parseInt(id.replace("follow_", ""));
            if(isNaN(userId)) {
                alert("Cannot perform this action.");
                return;
            }
            followUser(userId);
        });
    }

});