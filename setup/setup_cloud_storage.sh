echo "Setting Project ID: ${GOOGLE_CLOUD_PROJECT}"
gcloud config set project ${GOOGLE_CLOUD_PROJECT}

echo "Creating cloud storage bucket"
gcloud storage buckets create gs://one-click-deployment --project=${GOOGLE_CLOUD_PROJECT}

echo "Creating google-ads.yaml file"
echo "
client_customer_id: ${MCC_ID}
client_id: ${OAUTH_CLIENT_ID}
client_secret: ${OAUTH_CLIENT_SECRET}
refresh_token: ${REFRESH_TOKEN}
developer_token: ${DEVELOPER_TOKEN}
" >> google-ads.yaml

echo "Writing google-ads.yaml file to cloud storage bucket"
gcloud storage cp ./google-ads.yaml gs://one-click-deployment