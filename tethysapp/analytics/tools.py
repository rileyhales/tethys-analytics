def applist():
    """
    Using both the app harvester and some of the methodology used by the harvester, create a dictionary relating the
    name of the app according to tethys to the app package name which should be what is used in the app URL's
    """
    import pprint, os

    from tethys_apps.app_harvester import SingletonAppHarvester as AppHarvester
    harvester = AppHarvester()
    AppHarvester.harvest_apps(harvester)
    app_names = harvester.apps     # a list with all the apps as collected by the portal
    # pprint.pprint(app_names)

    from tethys_apps.tethysapp import __path__ as tethys_app_dir  # for getting the list of package names
    app_pkg_names = os.listdir(tethys_app_dir[0])
    app_pkg_names.remove('__init__.py')
    app_pkg_names.remove('__init__.pyc')
    app_pkg_names.remove('.gitignore')
    # pprint.pprint(app_pkg_names)

    apps = {}
    for i in range(len(app_names)):
        name = str(app_names[i]).replace('<TethysApp: ', '')    # force a string so that JsonResponse works
        name = name.replace('>', '')
        apps[name] = app_pkg_names[i]
    # pprint.pprint(apps)

    return apps


def generate_app_urls(request, apps_dict):
    """
    This fucntion creates urls for every app installed on the portal this app is on.

    Use this app in the controller for every navigable page so that the list of app links is visible in the navigation
    pane of that page. In base.html, there is a conditional set of django tags that will load the links if you give it
    this list of links and otherwise not.

    :param request: You need to give it the request passed to the controller of the page you're on (in the controller)
            so that that it knows what the base of the urls is supposed to be. then it manually adds urls using the
            lamda function.
    :param apps_dict: this is the dictionary containing app full names and package names that you get from the applist()
            function also found in tools.py
    :return: site_urls which is a list of dictionaries. Each dictionary contains the name, url, and active (a boolean
            check whether or not the current url is the url generated.
    """

    from django.contrib.sites.shortcuts import get_current_site
    from django.conf import settings

    apps = []
    for app in apps_dict:
        apps.append(apps_dict[app])

    current_site = get_current_site(request)

    if (settings.FORCE_SCRIPT_NAME):
        base = settings.FORCE_SCRIPT_NAME
    else:
        base = str(current_site);
    site_urls = list(map((lambda x: {
        'name': x,
        'url': request.build_absolute_uri(
            '//' + base + '/apps/analytics/stats/' + x.replace(" ", "_") + '/'),
        'active': x == request.path
    }), apps))

    return site_urls