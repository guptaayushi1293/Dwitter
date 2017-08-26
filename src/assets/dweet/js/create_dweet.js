$(document).ready(function() {
    $("#addCommentModal").addClass('hide');
    if($("#create_dweet").length) {
        $("#create_dweet").click(function() {
            var content = document.getElementById("dweet_content").value;
            if(content == "" || content == undefined) {
                alert("Tweet content cannot be empty.");
                return;
            }
            if(content.length > 140) {
                alert("Your total number of characters : " + content.length + " exceeds 140.");
                return;
            }
            else {
                //post ajax request
                addDweet(content);
            }
        });
    }

    if($(".dweet_comment_btn").length) {
        $(".dweet_comment_btn").click(function() {
            var buttonId = this.id;
            var dweetId = parseInt(buttonId.replace("comment_" ,""));
            addCommentToDweet(dweetId);
        });
    }

    if($(".dweet_like_btn").length) {
        $(".dweet_like_btn").click(function() {
            var buttonId = this.id;
            var dweetId = parseInt(buttonId.replace("like_" ,""));
            likeDweet(dweetId);
        });
    }
});

function addDweet(content) {
    var data = {};
    data['content'] = content;
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

function addCommentToDweet(dweetId) {
    var comments = getCommentsForDweet(dweetId);
    if($("#addCommentModal").length) {
        $("#addCommentModal").removeClass('hide');
        $("#addCommentModal").find(".modal-title").html('');
        $("#addCommentModal").find(".modal-body").html('');
        $("#addCommentModal").find(".modal-title").html("Reply to " + window.username);
        var previousCommentDivs = "";
        for(var i = 0; i < comments.length; i++) {
            var currentComment = comments[i];
            previousCommentDivs += "<div class='prev-comment-div' id='prev-comment-'" + currentComment['id'] + "'>" +
                            "<div class='comment-log-div'><label style='width:60%;'>" + currentComment['username']+ "</label>" +
                            "<label style='color:grey; width:40%;'>" + new Date(currentComment['commented_at']).toLocaleString() +"</label></div>" +
                            "<div><p>" + currentComment['content'] +"</p></div>" +
                            "</div>";
        }
        var addCommentDiv = "<div class='comment_div'>" +
                    "<textarea rows='3' cols='55' placeholder='Reply...'></textarea></div>";
        $("#addCommentModal").find(".modal-body").append(previousCommentDivs);
        $("#addCommentModal").find(".modal-body").append(addCommentDiv);
        var replyButton = $("#addCommentModal").find("#reply")[0];
        replyButton.addEventListener("click", function() {
            replyButton.disabled = true;
            var commentContent = $("#addCommentModal").find(".modal-body").find(".comment_div").find("textarea")[0].value;
            if(commentContent == "" || commentContent == null) {
                alert("A comment cannot be empty.");
                return;
            }
            saveCommentToDweet(dweetId, commentContent);
            replyButton.disabled = false;
        });
        $('#addCommentModal').modal({keyboard: false});
        $('#addCommentModal').fadeIn('slow');
    }
}

function saveCommentToDweet(dweetId, comment) {
    var data = {};
    data['dweetId'] = dweetId;
    data['content'] = comment;
    try {
        $.ajax({
            url: "/dweet/comment/add/",
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
        console.log("Exception occurred while commenting on a dweet : " + ex.toString());
    }
}

function getCommentsForDweet(dweetId) {
    var commentList = [];
    try {
        $.ajax({
            url: "/dweet/comment/" + dweetId + "/",
            type: "GET",
            async: false,
            success: function(response) {
                if(response['statusCode'] == 0) {
                    commentList = JSON.parse(response['comments']);
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
        console.log("Exception occurred while getting comments for a dweet : " + ex.toString());
    }
    return commentList;
}

function likeDweet(dweetId) {
    var data = {};
    data['dweet_id'] = dweetId;
    console.log(data);
    try {
        $.ajax({
            url: "/dweet/like/",
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
        console.log("Exception occurred while liking a tweet : " + ex.toString());
    }
}