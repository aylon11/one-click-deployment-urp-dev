#!/bin/bash

# Set Project ID
echo "Setting Project ID: ${GOOGLE_CLOUD_PROJECT}"
gcloud config set project ${GOOGLE_CLOUD_PROJECT}

# Enable Ads API
echo "Enabling Google Ads API..."
gcloud services enable googleads.googleapis.com

OAUTH_CALLBACK_URL=${SERVICE_URL}/oauth2callback

echo "Add the following URL to your OAuth Client ID's 'Authorized redirect URIs':" ${OAUTH_CALLBACK_URL}