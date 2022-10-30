# AccountsFetcher

This is a **demo app** to be used as a reference architecture for ads-api 
based cloud solutions.
This app deploys on GCP Cloud Run, and creates a web interface to fetch 
the user's Google Ads accounts.

This repository is intended to be a reference for future cloud based 
solutions developed in our team.

## Prerequisites

1. [Obtain a Google Ads Developer 
token](https://developers.google.com/google-ads/api/docs/first-call/dev-token#:~:text=A%20developer%20token%20from%20Google,SETTINGS%20%3E%20SETUP%20%3E%20API%20Center.)

1. Create a GCP project

## Setup

1. Create an [OAuth Consent 
Screen](https://console.cloud.google.com/apis/credentials/consent)

1. Make it of type "**External**"

1. Add all users you want to have access to the app

1. Create an [OAuth Client 
ID](https://console.cloud.google.com/apis/credentials/oauthclient)

1. Set Application type to "**Web application**"

1. Set the name to "**Accounts Fetcher**"

1. Take note of the **Client ID** and **Client Secret** presented to you

1. Click the big blue button to deploy:

   [![Run on Google 
Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run?revision=sso)

1. Choose the Google Cloud Project where you want to deploy the app

1. Select the region where you want to deploy

1. When deployment finishes, copy the app's URL

1. Go back to your OAuth2 Credentials and add `<YOUR_URL>/oauth2callback` 
to 'Authorized redirect URIs'

## Login

1. Open your app's URL in the browser

1. Go to 'Login' tab

1. Enter your credentials and sign in with your Google account - Make sure 
to log-in with a user that has access to your ads account.

1. You are all set! Go to 'Accounts' tab and see a list of all your 
accounts





