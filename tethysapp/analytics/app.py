from tethys_sdk.base import TethysAppBase, url_map_maker
from django.core.management import settings
import os


class Analytics(TethysAppBase):
    """
    Tethys app class for Portal Analytics Viewer.
    """

    name = 'Portal Analytics Viewer'
    index = 'analytics:home'
    icon = 'analytics/images/analytics_icon.png'
    package = 'analytics'
    root_url = 'analytics'
    color = '#d4af37'
    description = 'View usage statistics as tracked by Google Analytics for configured apps on this portal'
    tags = ''
    enable_feedback = False
    feedback_emails = []

    # This is the code that checks to see if django analytics is installed. If it is it adds the tags to implement it
    my_directory = os.path.dirname(__file__)
    with open(os.path.join(my_directory, 'templates/analytics/analytics.html'), 'w') as file:
        if 'analytical' in settings.INSTALLED_APPS:
            file.write("{% load google_analytics_js %}{% google_analytics_js %}")

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            # VIEWABLE PAGES
            UrlMap(
                name='home',
                url='analytics',
                controller='analytics.controllers.home'
            ),
            UrlMap(
                name='config',
                url='analytics/config',
                controller='analytics.controllers.config',
            ),
            UrlMap(                             # this is the controller for the page that shows app specific stats
                name='template',                # {name} is an argument the controller needs to accept second
                url='analytics/stats/{name}',
                controller='analytics.controllers.app_template'
            ),

            # AJAX CONTROLLERS
            UrlMap(
                name='get_app_list',
                url='analytics/ajax/get_applist',
                controller='analytics.ajaxhandlers.get_applist',
            ),
            UrlMap(
                name='stats',
                url='analytics/ajax/stats',
                controller='analytics.ajaxhandlers.analytics',
            ),
        )

        return url_maps
