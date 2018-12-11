// Getting the csrf token
let csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



$(document).ready(function() {
    // load parts of the page depending on which page you're on
    url = window.location.href;
    console.log(url);

    if (url.endsWith("/apps/analytics/")) {
        map();
        installed_apps = retrieve_app_list();

        for (app in installed_apps) {
            list_item = '<li>' + app + '</li>';
            $("#apps").append(list_item);
        };
    }
    if (url.includes("analytics/stats")) {
        app_page_stats(url);
    }

    $("#submit_request").on('click', function() {
        requester();
        });


});