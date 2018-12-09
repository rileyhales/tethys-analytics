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

function get_stats() {
    $.ajax({
        url:'/apps/analytics/ajax/stats/',
        async: false,
        data: 'give me the stats',
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(result) {
            stats = result;
            return stats
            },
        });
    return stats
}

function requester() {
    $("#apiData").text('Please wait while the analytics data is retrieved...');
    data = {
        'metrics': $("#metrics").val(),
        'dimensions': $("#dimensions").val(),
    }

    $.ajax({
        url:'/apps/analytics/ajax/requester/',
        async: true,
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json',
        method: 'POST',
        success: function(result) {
//            $("#apiData").text(JSON.stringify(result));
            $('pre').html(JSON.stringify(result, undefined, 2));
            return result
            }
        });
}
