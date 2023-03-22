$(document).ready(function() {
    $('.btn-confirm-delete').click(function() {
        return confirm('Are you sure? Deleting restaurants is permanent!');
    });
});