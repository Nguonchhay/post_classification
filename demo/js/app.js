(function ($) {
  // USE STRICT
  "use strict";

    var baseUrl = 'http://0.0.0.0:8080';

    $('#btnTrain').click(function() {
        var url = baseUrl + '/training';
        var message = $('#message');
        message.html('Start training...');
        $.ajax({
            url: url,
            method: 'POST',
            dataType: 'json',
            contentType: "application/json; charset=utf-8"
        }).done(function(res) {
            console.log(res)
            message.html('Training is done.');
        });
    });

    $('#btnClassify').click(function() {
        var sentence = $('#sentence').val();
        var url = baseUrl + '/classify';
        var message = $('#message');
        var navTab = $('#nav-tab');
        var navTabContent = $('#nav-tabContent');
        var tabTitles = '';
        var tabContents = ''

        if (sentence != '') {
            message.html('Searching ...');
            navTab.html(tabTitles);
            navTabContent.html(tabContents);

            $.ajax({
                url: url,
                data: JSON.stringify({
                    sentence: sentence
                }),
                method: 'POST',
                dataType: 'json',
                contentType: "application/json; charset=utf-8"
            }).done(function(res) {
                var category = res.data.category;
                $('#categoryName').html(category.name);

                var startTime = parseFloat(res.data.start_time);
                var endTime = parseFloat(res.data.end_time);
                var elapseTime = (endTime - startTime).toFixed(4);
                $('#executeTime').html(parseInt(elapseTime));

                message.html('Rendering to UI ...');
                var news = res.data.news;
                $.each(news, function(index, item) {
                    tabTitles += '<a class="nav-item nav-link ' + (index == 0 ? 'active' : '') + ' show" id="custom-nav-tab-' + index + '" data-toggle="tab" href="#custom-nav-' + index + '" role="tab" aria-controls="custom-nav-home" aria-selected="true">' + item[1] + '(' + item[0] + ')</a>';

                    tabContents += '<div class="tab-pane fade ' + (index == 0 ? 'active' : '') + ' show" id="custom-nav-' + index + '" role="tabpanel" aria-labelledby="custom-nav-tab-' + index + '">';
                        tabContents += '<div class="au-task-list js-scrollbar3">'
                        $.each(item[2], function(indexNews, newsRecord) {
                            tabContents += '<div class="au-task__item-inner"><h3 class="task">' + newsRecord[2] + '</h3><p>' + newsRecord[3] + '</p></div>';
                        });
                    tabContents += '</div></div>';
                });
                navTab.html(tabTitles);
                navTabContent.html(tabContents);

                message.html('');
            });
        }
    });

})(jQuery);