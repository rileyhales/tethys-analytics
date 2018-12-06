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