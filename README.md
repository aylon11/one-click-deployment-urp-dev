# If This Then Ad

[![build](https://img.shields.io/badge/build-passing-brightgreen?style=flat&logo=github)](https://github.com/google/if-this-then-ad)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/google/if-this-then-ad?label=release&logo=github)](https://github.com/google/if-this-then-ad)
[![GitHub last commit](https://img.shields.io/github/last-commit/google/if-this-then-ad)](https://github.com/google/if-this-then-ad/commits)

## Setup

1. Create an [OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent)

1. Make it of type "**External**"

1. Add all users you want to have access to the app

1. Create an [OAuth Client ID](https://console.cloud.google.com/apis/credentials/oauthclient)

1. Set Application type to "**Web application**"

1. Set the name to "**Accounts Fetcher**"

1. Take note of the **Client ID** and **Client Secret** presented to you

1. Click the big blue button to deploy:

   [![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run?revision=sso)

1. Choose the Google Cloud Project where you want to deploy the app

1. Select the region where you want to deploy

1. When deployment finishes, copy the app's URL

1. Go back to your OAuth2 Credentials and add `<YOUR_URL>/oauth2callback` to 'Authorized redirect URIs'



