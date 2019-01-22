<h1>Tethys Portal Analytics Viewer App</h1>

<p> The Tethys Portal Analytics Viewer App allows portal administrators to track and visualize the usage of Tethys applications for Tethys 2.1 and later. Analytics data are provided by Google Analytics and implemented in the Tethys environment using the Django-Analytical python package. For information about these services, refer to:</p>
<li><b>Tethys:</b> <a href="http://www.tethysplatform.org/" target="_blank">http://www.tethysplatform.org/</a>
<li><b>Google Analytics:</b> <a href="https://analytics.google.com/" target="_blank">https://analytics.google.com/</a>
<li><b>Django-Analytical:</b> <a href="https://github.com/jazzband/django-analytical" target="_blank">https://github.com/jazzband/django-analytical</a>

<p>This application was built by Riley Hales at the Brigham Young University Hydroinformatics Lab, 2019.


<h2>Security Warnings</h2>
<p>If you modify this app and use GitHub to track your changes, you need to exclude the Google Analytics API key from your commits for security reasons. If you forget, you should immediately return to <a target="_blank" href="console.developers.google.com">console.developers.google.com</a> and deauthorize that key. Follow the instructions below to set up a new analytics reporting service account and generate a new key. If you followed these instructions, the key should only be valid for queries, not modifications of your Google account so your account will remain safe but you will leak personal information.</p>
<p>By using this app and creating Google Analytics accounts, you will agree to the responsible use of the information gathered about your users. You should follow any applicable best practices to ensure this information is not made publicly available or misused.</p> 


<h2>Configuration Instructions</h2>
 
 <p>Before using this app, you should do two things: 1) setup Google Analytics credentials and downloaded an api key, 2) make sure you have added the django-analytical package to the list of installed apps on your portal and specified a property ID.</p>

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


<h2>Making Tethys Apps trackable</h2>

  <p>To make an app trackable using the portal's configuration, you need to modify app.py and base.html. The following is an explanation of the code proposed as an addition to the base tethys templates used to scaffold a new app.</p>
  <p>If this propose change to the app templates is accepted, then developers shouldn't have to do any work to make tracking work for their applications.
  
  <ol>
    <li>Check to see if Django-Analytical is installed on the portal. Add a property to the app class in app.py with the boolean result of this check.
        <ul>
            <li>The property is called analytics. It is a boolean check to see if the Django-Analytical package has been installed on the portal. It is important that it be referenced this way so that this app can check the configuration status of other apps installed on the portal easily. <code>analytics = bool('analytical' in settings.INSTALLED_APPS and settings.GOOGLE_ANALYTICS_JS_PROPERTY_ID)</code></li>
        </ul>            
    <li>Write the django tags that implement the tracking script to analytics.html based on the value of the app.analytics value from step 1. This is probably best placed in the __init__ function for the class.</li>
    <li>In base.html, under the block scripts tag, add the line {% include analytics.html %}. Because of the way the code was written, this will be empty if the check was false and have the tags if the code is true. This will not interfere with app performance regardless of the contents.
  </ol>
