function retrieve_app_list() {
    $.ajax({
        url:'/apps/analytics/ajax/get_applist/',
        async: false,
        data: 'give me your app list',
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(result) {
            installed_apps = result;
            return installed_apps
            },
        });
    return installed_apps
}

function app_page_stats(url) {
    $.ajax({
        url:'/apps/analytics/ajax/stats/',
        async: false,
        data: JSON.stringify({'url': url}),
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(result) {
            console.log(result)
            $("#users").text(result['users']);
//            $("#users7").text(result['users7']);
//            $("#users28").text(result['users28']);
            $("#sessions").text(result['sessions']);
            $("#averageTime").text(result['avgSessionDuration']);
            },
        });
}

function requester() {
    $("#apiData").text('Please wait while the analytics data is retrieved...');
    data = {
        'metrics': $("#metrics").val(),
        'dimensions': $("#dimensions").val(),
    }

    console.log(data);

    $.ajax({
        url:'/apps/analytics/ajax/requester/',
        async: true,
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json',
        method: 'POST',
        success: function(result) {
            $('pre').html(JSON.stringify(result, undefined, 2));
            return result
            }
        });
}
