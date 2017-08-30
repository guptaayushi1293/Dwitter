$(document).ready(function() {
    if($(".follow_btn").length) {
        $(".follow_btn").click(function() {
            var buttonId = this.id;
            var followUserId = parseInt(buttonId.replace("follow_", ""));
            followUser(followUserId);
        });
    }
});