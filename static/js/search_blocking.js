// if the user has not clicked the search button yet
let first_attempt = true;
// boolean for if the search button is disabled
let disabled = $("#search-btn").prop("disabled"); 

$(document).ready(function() {
    $("#search-btn").click(function() {
        let search_bar = document.getElementById("search-bar");
        let query = search_bar.value;
        // if the number of characters typed is less than 3
        if (query.length < 3 && !disabled) {
            $("#search-bar").focus();
            // disable the search button
            $("#search-btn").prop("disabled", true);
            alert("Your search must be at least 3 characters long");
            // user must now type 3 characters before the search button is enabled
            first_attempt = false;
        }
    });
});

$(document).ready(function() {
    $("#search-bar").on("input", function() {
        if (this.value.length >= 3) {
            // once the user has typed 3 characters the search button is enabled
            $("#search-btn").prop("disabled", false);
        } else if (!first_attempt) {
            // until then it is disabled
            $("#search-btn").prop("disabled", true);
        }
    });
});