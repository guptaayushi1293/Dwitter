$(document).ready(function() {
    if($(".unfollow_btn").length) {
        $(".unfollow_btn").click(function() {
            var buttonId = this.id;
            var followingUserId = parseInt(buttonId.replace("unfollow_", ""));
            unFollowUser(followingUserId);
        });
    }
});