# privacy-portal-integration
SSO Integration with Privacy Portal Using tutorial on `https://privacyportal.org/blog/sign-in-with-privacy-portal-tutorial`

# Requirements
- Create a new account on Privacy Portal `https://app.privacyportal.org/`
- Go to the developer settings and create an application
- In the callback_url of the application, add the url `{your app host}/auth/callback` - This page is already provided in the app

# Setup
- Create your .env and add the privacy portal client id and client secret
- portal client id and client secret can be gotten from the Privacy Portal Application Credentials

# Development Setup
- Create a virtual environmnet on your system
- Pull the repo
- Run `pip install -r requirements.txt`
- Run `python manage.py runserver` to start the app
- Visit `{your app host}/auth/home` then click on the Login With Privacy Portal button
- NOTE - Use a client like ngrok to create a test domain to tunnel to your app, this should be `your app host`
