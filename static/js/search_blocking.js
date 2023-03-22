let first_attempt = true;
let disabled = $("#search-btn").prop("disabled");

$(document).ready(function() {
    $("#search-btn").click(function() {
        let search_bar = document.getElementById("search-bar");
        let query = search_bar.value;
        if (query.length < 3 && !disabled) {
            $("#search-bar").focus();
            $("#search-btn").prop("disabled", true);
            alert("Your search must be at least 3 characters long");
            first_attempt = false;
        }
    });
});

$(document).ready(function() {
    $("#search-bar").on("input", function() {
        if (this.value.length >= 3) {
            $("#search-btn").prop("disabled", false);
        } else if (!first_attempt) {
            $("#search-btn").prop("disabled", true);
        }
    });
});