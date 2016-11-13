/**
 * Created by Samuel on 11/6/2016.
 */

// TODO: CHANGE LOGIN METHOD TO USERNAME & PASSWORD
$(function() {
    // variable declarations
    var token = "";
    var $token = $('#token');
    var $loginButton = $('#login-button');
    var $devToken = $('#dev-token');

    // respond to login
    $loginButton.on('click', function() {
        if ($token.val() != "")
            $.ajax({
                url : '/wiki/token',
                method : 'POST',
                data: {
                    token: $token.val()
                },
                success: function() {
                    window.location.href = '/';
                }
            });
    });

    $devToken.on('click', function() {
        $token.val('replace with your own token');
    });
});