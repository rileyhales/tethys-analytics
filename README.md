<h1>Tethys Portal Analytics Viewer App</h1>

<p> The Tethys Portal Analytics Viewer App allows portal administrators to track and visualize the usage of Tethys applications for Tethys 2.1 and later. Analytics data are provided by Google Analytics and and implemented in the Tethys environment using the Django-Analytical python package. For information about these services, refer to:</p>
<li><b>Tethys:</b> <a href="http://www.tethysplatform.org/" target="_blank">http://www.tethysplatform.org/</a>
<li><b>Google Analytics:</b> <a href="https://analytics.google.com/" target="_blank">https://analytics.google.com/</a>
<li><b>Django-Analytical:</b> <a href="https://github.com/jazzband/django-analytical" target="_blank">https://github.com/jazzband/django-analytical</a>

<p>This application was built by Riley Hales at the Brigham Young University Hydroinformatics Lab, 2019.


<h2>Configuration Instructions</h2>
 
 <p>Before using this app, you should do three things: 1) setup Google Analytics credentials and downloaded an api key, 2) make sure you have added the django-analytical package to the list of installed apps on your portal and specified a property ID, 3) and added the logical check to each of the apps on your portal to enable tracking for that app.</p>

  <h3>1. Setup a Google Analytics for your portal</h3>
    <ol>
      <li>Go to <a target="_blank" href="console.developers.google.com">console.developers.google.com</a></li>
      <li>Go to the APIs and Services section and find the Credentials tab</li>
      <li>Create new credentials -> Service Account Key -> New service account
        <ul>
          <li>Name the service account getmetrics</li>
          <li>Role: Project Owner</li>
          <li>Note the service account ID email address listed. copy this address.</li>
          <li>Choose JSON for your key type.</li>
          <li><b>DO NOT LOSE THIS KEY. YOU CANNOT GET ANOTHER COPY.</b></li>
          <li>Make a copy that you can put in the analytics app's 'app workspace' folder. name it api_info.json</li>
        </ul>
      </li>
      <li>Return to the IAM & Admin section and go to the IAM tab</li>
      <li>Add a new member.
        <ul>
          <li>Use the email address from the previous steps. It should prompt you to use that as you begin typing</li>
          <li>Choose Project Owner as the role.</li>
          <li>Save</li>
        </ul>
      <li>Go to <a target="_blank" href="analytics.google.com">analytics.google.com</a></li>
      <li>In admin settings, find the User Management section for the <i>account</i> (not property or view).</li>
      <li>Add a new user with the email address you got from the previous steps. Grant Read & Analyze permissions.</li>
      <li>Wait at least 5 minutes before making requests.</li>
    </ol>


  <h3>2. Configuring the Portal</h3>
  <p>Tethys Portals can be configured to track app usage of configured apps using the Django-Analytical python package.
    <ul>
      <li><a target="_blank" href="https://django-analytical.readthedocs.io/en/latest">Read the Documentation on ReadTheDocs</a> </li>
      <li><a target="_blank" href="https://github.com/jazzband/django-analytical">View the source code on GitHub</a> </li>
    </ul>
  </p>
  <ol>
    <li>Install Django-Analytical
      <ul>
        <li>Open the command line for the server</li>
        <li>Enter the tethys python environment with the shortcut alias 't'</li>
        <li>conda install django-analytical</li>
      </ul>
    </li>
    <li>Configure the portal's settings.py file
      <ul>
        <li>The settings.py file is found in .../tethys/src/tethys_portal/settings.py</li>
        <li>Find the INSTALLED_APPS = () tuple (should contain about a dozen package names)</li>
        <li>Above that tuple, add GOOGLE_ANALYTICS_JS_PROPERTY_ID = 'UA-12345678-9' replacing the ID with the one generated for you by Google</li>
        <li>Add 'analytical' as the last element of the INSTALLED_APPS tuple</li>
      </ul>
    </li>
  </ol>


  <h3>3. Configuring an App</h3>
  <p>To make an app trackable using the portal's configuration, you need to create a new html file, modify app.py, and modify base.py.</p>
  <ol>
    <li>Create a new html document
      <ul>
        <li>Create a new, blank html document, called analytics.html, in the templates folder of the app. Do not add anything to this document.</li>
      </ul>
    </li>
    <li>App.py
      <ul>
        <li>
          Add an import statement: from django.core.management import settings<br>
          This imports the settings.py file of the tethys portal where you added the analytical python package to the list of installed apps and listed the tracking ID.<br>
        </li>
        <li>
          Add the following 4 lines of code. Put it in the class and beneath the declaration of name, color, etc.<br>
          <p>
            app_file_path = os.path.dirname(__file__)<br>
            with open(os.path.join(app_file_path, 'templates/[name of your app package]/analytics.html'), 'w') as file:<br>
            if 'analytical' in settings.INSTALLED_APPS:<br>
            file.write("{% load google_analytics_js %}{% google_analytics_js %}")
          </p>
        </li>
        <li>
            This code gets the file path of app.py. Then it uses that to open the analytics.html file you created.
            make sure you appropriately edit the arguments in os.path.join() to get the correct file path of the
            template. When the code opens this document, all the contents of the file are erased. Next it checks if
            the analytical package is installed to the portal. If it is, it adds the django tags to the html file.
        </li>
      </ul>
    </li>
    <li>Modify base.html
      <ul>
        <li>Open base.html</li>
        <li>Under the "block scripts" tag, add include "[name of your app package]/analytics.html"</li>
        <li>
            The include tag lets you use the entire contents of the analytics.html file where you wrote the tag. This
            will either be a blank document, having no effect, or a document containing the tags to implement Google
            Analytics.
        </li>
      </ul>
    </li>
  </ol>