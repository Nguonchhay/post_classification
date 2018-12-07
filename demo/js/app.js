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
            $('#categoryName').html('');
            $('#executeTime').html('');
            $('#existingKeyword').html('');
            $('#newKeyword').html('');

            $.ajax({
                url: url,
                data: JSON.stringify({
                    sentence: sentence
                }),
                method: 'POST',
                dataType: 'json',
                contentType: "application/json; charset=utf-8"
            }).done(function(res) {
                message.html('Rendering to UI ...');
                if (res.data.category === undefined) {
                    message.html('There is no category was found. Please try another sentence.');
                } else {
                    var category = res.data.category;
                    $('#categoryName').html(category.name);

                    // Calculate execute time
                    var startTime = parseFloat(res.data.start_time);
                    var endTime = parseFloat(res.data.end_time);
                    var elapseTime = (endTime - startTime);
                    $('#executeTime').html(elapseTime.toFixed(4));

                    // Find existing or new keywords
                    var newsKeywords = res.data.news_keywords;
                    var existingKeywords = '';
                    var newKeywords = '';
                    $.each(newsKeywords, function(keyword, keywordData) {
                        if (keywordData.word !== undefined) {
                            newKeywords += keyword + ' , ';
                        } else {
                            existingKeywords += keyword + ' , ';
                        }
                    });

                    if (existingKeywords != '') {
                        existingKeywords = existingKeywords.slice(0, -2);
                    }

                    if (newKeywords != '') {
                        newKeywords = newKeywords.slice(0, -2);
                    }

                    $('#existingKeyword').html(existingKeywords);
                    $('#newKeyword').html(newKeywords);

                    // Rendering News
                    var news = res.data.news;
                    $.each(news, function(index, item) {
                        tabTitles += '<a class="nav-item nav-link ' + (index == 0 ? 'active' : '') + ' show" id="custom-nav-tab-' + index + '" data-toggle="tab" href="#custom-nav-' + index + '" role="tab" aria-controls="custom-nav-home" aria-selected="true">' + item[1] + '(' + item[0] + ')</a>';

                        tabContents += '<div class="tab-pane fade ' + (index == 0 ? 'active' : '') + ' show" id="custom-nav-' + index + '" role="tabpanel" aria-labelledby="custom-nav-tab-' + index + '">';
                            tabContents += '<div class="au-task-list js-scrollbar3">'
                            var newsNum = 1;
                            $.each(item[2], function(indexNews, newsRecord) {
                                tabContents += '<div class="au-task__item-inner"><h3 class="task">' + (newsNum++) + '. ' + newsRecord[2] + '</h3><p>' + newsRecord[3] + '</p></div>';
                            });
                        tabContents += '</div></div>';
                    });
                    navTab.html(tabTitles);
                    navTabContent.html(tabContents);

                    message.html('');
                }
            });
        }
    });

})(jQuery);