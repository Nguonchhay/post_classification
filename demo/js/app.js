(function ($) {
  // USE STRICT
  "use strict";

    var baseUrl = 'http://0.0.0.0:8080'

    $('#btnTrain').click(function() {
        var url = baseUrl + '/training';
        var message = $('#message');
        message.html('Start training...');
        $.ajax({
            url: url,
            method: 'POST',
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            traditional: true,
            async: false,
        }).done(function(res) {
            console.log(res)
            message.html('Training is done.');
        });
    });

})(jQuery);