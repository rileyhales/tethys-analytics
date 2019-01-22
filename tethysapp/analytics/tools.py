def applist():
    """
    Using both the app harvester and some of the methodology used by the harvester, create a dictionary relating the
    name of the app according to tethys to the app package name which should be what is used in the app URL's
    """
    import os

    from tethys_apps.harvester import SingletonHarvester as AppHarvester
    harvester = AppHarvester()
    AppHarvester.harvest_apps(harvester)
    app_names = harvester.apps     # a list with all the apps as collected by the portal

    from tethys_apps.tethysapp import __path__ as tethys_app_dir  # for getting the list of package names
    app_pkg_names = os.listdir(tethys_app_dir[0])
    app_pkg_names.remove('__init__.py')
    app_pkg_names.remove('__pycache__')
    app_pkg_names.remove('.gitignore')

    apps = {}
    for i in range(len(app_names)):
        name = str(app_names[i]).replace('<TethysApp: ', '')    # force a string so that JsonResponse works
        name = name.replace('>', '')
        apps[name] = app_pkg_names[i]

    return apps


def generate_app_urls(request, apps_dict):
    """
    This fucntion creates urls for every app installed on the portal this app is on.

    Use this app in the controller for every navigable page so that the list of app links is visible in the navigation
    pane of that page. In base.html, there is a conditional set of django tags that will load the links if you give it
    this list of links and otherwise not.

    :param request: You need to give it the request passed to the controller of the page you're on (in the controller)
            so that that it knows what the base of the urls is supposed to be. then it manually adds urls using the
            lamda function. the x for the lambda function is the app dictionary parameter
    :param apps_dict: this is the dictionary containing app full names and package names that you get from the applist()
            function also found in tools.py
    :return: site_urls which is a list of dictionaries. Each dictionary contains the name, url, and active (a boolean
            check whether or not the current url is the url generated). active needs to be this verbose otherwise the
            analytics app link will be highlighted all the time.
    """

    from django.contrib.sites.shortcuts import get_current_site
    from django.conf import settings

    current_site = get_current_site(request)

    if (settings.FORCE_SCRIPT_NAME):
        base = settings.FORCE_SCRIPT_NAME
    else:
        base = str(current_site);
    site_urls = list(map((lambda x: {
        'name': x,
        'url': request.build_absolute_uri(
            '//' + base + '/apps/analytics/stats/' + apps_dict[x].replace(" ", "_") + '/'),
        'active': request.path.endswith('stats/' + apps_dict[x] + '/')
    }), apps_dict))

    return site_urls


def supportedMetricsDimensions():
    supported = {
        'metrics': [
            'ga:users',
            'ga:7dayUsers',
            'ga:14dayUsers',
            'ga:28dayUsers',
            'ga:sessions',
            'ga:avgSessionDuration',
        ],
        'dimensions': [
            'ga:country',
            'ga:city',
            'ga:browser',
            'ga:pagePath',
            'ga:latitude',
            'ga:longitude',
            'ga:continent',
            'ga:city',
            'ga:cityId',
            'ga:countryIsoCode',
        ],
    }
    return supported