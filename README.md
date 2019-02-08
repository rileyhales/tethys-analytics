<h1>Tethys Portal Analytics Viewer App</h1>

<p> The Tethys Portal Analytics Viewer App allows portal administrators to track and visualize the usage of Tethys applications for Tethys 2.1 and later. Analytics data are provided by Google Analytics and implemented in the Tethys environment using the Django-Analytical python package. For information about these services, refer to:</p>
<li><b>Tethys:</b> <a href="http://www.tethysplatform.org/" target="_blank">http://www.tethysplatform.org/</a>
<li><b>Google Analytics:</b> <a href="https://analytics.google.com/" target="_blank">https://analytics.google.com/</a>
<li><b>Django-Analytical:</b> <a href="https://github.com/jazzband/django-analytical" target="_blank">https://github.com/jazzband/django-analytical</a>

<p>This application was built by Riley Hales at the Brigham Young University Hydroinformatics Lab, 2019.


<h2>Security Warnings</h2>
<p>If you modify this app and use GitHub to track your changes, you need to exclude the Google Analytics API key from your commits for security reasons. If you forget, you should immediately return to <a target="_blank" href="console.developers.google.com">console.developers.google.com</a> and deauthorize that key. Follow the instructions below to set up a new analytics reporting service account and generate a new key. If you followed these instructions, the key should only be valid for queries, not modifications of your Google account so your account will remain safe but you will leak personal information.</p>
<p>By using this app and creating Google Analytics accounts, you will agree to the responsible use of the information gathered about your users. You should follow any applicable best practices to ensure this information is not made publicly available or misused.</p> 


<h2>Preparing a Google Analytics account for Tethys</h2>
    <ol>
      <li>Go to <a target="_blank" href="console.developers.google.com">console.developers.google.com</a></li>
      <li>Go to the APIs and Services section and find the Credentials tab</li>
      <li>Create new credentials -> Service Account Key -> New service account
        <ul>
          <li>Name the service account getmetrics</li>
          <li>Role: Project Owner</li>
          <li>Note the service account ID email address listed. copy this address.</li>
          <li>If you want to use the Portal Analytics Tracking App to visualize metrics, you will need to get an API key. Choose JSON for your key type.</li>
          <li><b>DO NOT LOSE OR SHARE THIS KEY</b></li>
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
      <li>Add a new user with the email address you got from the previous steps. Grant Read & Analyze permissions. You will need to wait at least 5 minutes before making requests while these changes synchronize across Google's services.</li>
      <li>Create A New Property. Set the appropriate website name, URL, content category, time zone, etc. When you finish, you will get a "tracking-ID" in the format "UA-123456789-1". The 9 digits in the center are an identifier for your account and the "-1" corresponds to the number of the property you're tracking. Save this number for configuring your portal.</li>
      <li>In your tethys portal, navigate to the file "../tethys/src/tethys_portal/settings.py". In that file, you will find a line about half way down that says GOOGLE_ANALYTICS_JS_PROPERTY_ID = ''. Inside the single quotes, add your Tracking ID from the previous step. Save.'</li>
    </ol>


<h2>Special Instructions for  Tethys 3</h2>

<p>Beginning in Tethys 3 distributions, all the portal side setup for analytics have been automated. To use this app in Tethys 3 and to track apps created in Tethys 3, you need to have a properly set up Google Analytics account and have a copy of the API key to provide to the app in the 'app_workspace folder'. Make sure the key is name 'api_info.json'. </p>
<p><i>If apps do not track correctly, they may not have added the necessary code to implement tracking when upgrading from Tethys 2 to 3. Refer to the Special Instructions for Tethys 2.X and Tethys documentation to solve compatibility issues.</i></p>


<h2>Special Instructions for Tethys 2.X</h2>

<p>To track applications in Tethys 2 environments, you need to:
<ol>
    <li>Create a Google Analytics account as describe above</li>
    <li>Modify the applications to have django-analytical tracking tags</li>
    <li>Modify the portal's settings.py file to specifiy tracking ID's</li>
    </ol>

  <h3>Adapting Applications</h3>
  Modify app.py. This code will perform an automated check to see if Django-Analytical is the necessary django tags get added to the html scripts sections. Otherwise, they are cleared.
    <ol>
        <li>Modify app.py. Add the following class property: <code>analytics = bool('analytical' in settings.INSTALLED_APPS and settings.GOOGLE_ANALYTICS_JS_PROPERTY_ID)</code>. This is a boolean check to see if the portal is configured correctly. It is set up this way so that the Portal Analytics App can refer to the property later.</li>
        <li>Under the analytics class property you just added, you need to add 3 lines of code that write the django tags to the scripts section of the base template.
            <br><code>
                with open(os.path.join(os.path.dirname(__file__), 'templates/analytics/analytics.html'), 'w') as file:
                <blockquote>if analytics:
                <blockquote>file.write("{% load google_analytics_js %}{% google_analytics_js %}")
            </code>
        <li>Create a new blank html file with the rest of the templates called analytics.html.</li>
        <li>In base.html, under the block scripts tag, add the line {% include analytics.html %}. Because of the way the code was written, this will be empty if the check was false and have the tags if the code is true. This will not interfere with app performance regardless of the contents.</li>        
    </ol>
  
  <h3>Adding Django-Analytical</h3>
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



