(function ($) {
  // USE STRICT
  "use strict";

    var baseUrl = 'http://0.0.0.0:8080'

    $.ajax({
        url: baseUrl,
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        traditional: true,
        async: false,
    }).done(function(res) {
        console.log(res)
    });

})(jQuery);