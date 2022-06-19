from crypt import methods
from distutils.command.config import config
from io import UnsupportedOperation
import os
import yaml
import hashlib
import webbrowser
import socket
import sys
import re
import json
from urllib.parse import unquote
from google.ads.googleads.client import GoogleAdsClient
from flask import Flask, render_template, url_for, flash, redirect, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from google_auth_oauthlib.flow import Flow

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd5face11387058ea92b760a75b13caa4'

# UNCOMMENT WHEN RUNNINT LOCALLY
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

_YAML_FILE = './google-ads.yaml'
_SECRET_FILE = './secret.json'

_SCOPES = ["https://www.googleapis.com/auth/adwords"]


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/guide")
def guide():
    return render_template('guide.html')


@app.route("/accounts")
def accounts():
    client = create_client()
    return render_template('accounts.html', posts=get_accounts(client), )


@app.route("/login", methods=["POST","GET"])
def login():
    form = AuthenticationForm()
    if form.validate_on_submit():

        client_config = {
              'web': {
                'client_id': form.client_id.data,
                'client_secret': form.client_secret.data,
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://accounts.google.com/o/oauth2/token',
                'login_customer_id': int(form.mcc.data),
                'developer_token': form.developer_token.data
            }
        }

        with open(_SECRET_FILE, 'w') as f:
            json.dump(client_config, f)

        flow = Flow.from_client_config(client_config=client_config, scopes=_SCOPES)
        flow.redirect_uri = url_for('oauth2callback', _external=True, _scheme='https') 

        # Create an anti-forgery state token as described here:
        # https://developers.google.com/identity/protocols/OpenIDConnect#createxsrftoken
        passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()
        
        authorization_url, state = flow.authorization_url(
            access_type="offline",
            state=passthrough_val,
            prompt="consent",
            include_granted_scopes="true",
        )
        session['state'] = state


        return redirect(authorization_url)

    return render_template('login.html', form=form)



@app.route('/oauth2callback')
def oauth2callback():
  state = session['state']

  flow = Flow.from_client_secrets_file(client_secrets_file=_SECRET_FILE, scopes=None, state=state)
  flow.redirect_uri = url_for('oauth2callback', _external=True, _scheme='https')

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = request.url

  flow.fetch_token(authorization_response=authorization_response.replace('http', 'https'))

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  session['credentials'] = credentials_to_dict(credentials)

  with open(_SECRET_FILE, 'r') as f:
      creds = json.load(f)
      creds = creds['web']

  config = {
            'client_id' : creds['client_id'],
            'client_secret': creds['client_secret'],
            'developer_token': creds['developer_token'],
            'login_customer_id': creds['login_customer_id'],
            'refresh_token': credentials.refresh_token,
            'use_proto_plus': True
        }
    

  with open(_YAML_FILE, 'w') as f:
      yaml.dump(config, f)

  return redirect(url_for('home'))


def create_client():
    try:
        googleads_client = GoogleAdsClient.load_from_storage(
            './google-ads.yaml', version="v11")
    
        # test credentials valid
        get_accounts(googleads_client)
        return googleads_client
    except Exception as e:
        return 0


def get_accounts(client):
    accounts = []
    try:
        with open(_YAML_FILE, 'r') as f:
            config = yaml.load(f,Loader=yaml.SafeLoader)
        customer_id = config['login_customer_id']
        
        ga_service = client.get_service("GoogleAdsService")
        query = """
                SELECT
                customer_client.descriptive_name,
                customer_client.id
            FROM
                customer_client
            WHERE
                customer_client.manager = False
            ORDER BY customer_client.id LIMIT 10
        """
        stream = ga_service.search_stream(customer_id=str(customer_id), query=query)
        for batch in stream:
            for row in batch.results:
                accounts.append({
                'name': row.customer_client.descriptive_name,
                'id': row.customer_client.id})
    except Exception as e:
        accounts.append({
            'name': 'Credentials not set / are not correct',
            'id': 'Please set up credentials in login page'
        })
    return accounts


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


class AuthenticationForm(FlaskForm):
    validators = [DataRequired()]
    client_id = StringField('Client ID', validators=validators)
    client_secret = StringField('Client Secret', validators=validators)
    developer_token = StringField('Developer Token', validators=validators)
    mcc = StringField('MCC ID', validators=validators)
    submit = SubmitField('Set Credentials')


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=int(os.environ.get("PORT", 8080)))