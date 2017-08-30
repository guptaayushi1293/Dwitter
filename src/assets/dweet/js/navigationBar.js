$(document).ready(function() {
    if ($("#id_search_link").length) {
        $("#id_search_link").click(function() {
            var searchText = $("#id_search_bar").val();
            if (searchText == "" || searchText == undefined) {
                alert("Please fill some text to search dweet or user.");
                return;
            }
            $('#id_search_link').attr('href',"/dweet/search/" + searchText + "/");
        });
    }
});