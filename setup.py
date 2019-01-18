import os
import sys
from setuptools import setup, find_packages
from tethys_apps.app_installation import custom_develop_command, custom_install_command

### Apps Definition ###
app_package = 'analytics'
release_package = 'tethysapp-' + app_package
app_class = 'analytics.app:Analytics'
app_package_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tethysapp', app_package)

### Python Dependencies ###
dependencies = ['google-api-python-client', 'apiclient', 'oauth2client', 'pprint', 'geojson']

setup(
    name=release_package,
    version='0.0.1',
    tags='',
    description='View usage statistics as tracked by Google Analytics for configured apps on this portal',
    long_description='',
    keywords='',
    author='Riley Hales',
    author_email='',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['tethysapp', 'tethysapp.' + app_package],
    include_package_data=True,
    zip_safe=False,
    install_requires=dependencies,
    cmdclass={
        'install': custom_install_command(app_package, app_package_dir, dependencies),
        'develop': custom_develop_command(app_package, app_package_dir, dependencies)
    }
)
