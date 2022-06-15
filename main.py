from crypt import methods
from distutils.command.config import config
from io import UnsupportedOperation
import os
import yaml
from google.ads.googleads.client import GoogleAdsClient
from flask import Flask, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd5face11387058ea92b760a75b13caa4'

_YAML_FILE = './google-ads.yaml'


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
        config = {
            'client_id' : form.client_id.data,
            'client_secret': form.client_secret.data,
            'refresh_token': form.refresh_token.data,
            'developer_token': form.developer_token.data,
            'login_customer_id': int(form.mcc.data),
            'use_proto_plus': True
        }

        with open(_YAML_FILE, 'w') as f:
            yaml.dump(config, f)

        if not create_client():
            flash('Invalid Credentials',category='danger')
        else:
            flash(f'Credentials Valid', category='success')
            return redirect(url_for('home'))   

    return render_template('login.html', form=form)


def create_client():
    try:
        googleads_client = GoogleAdsClient.load_from_storage(
            './google-ads.yaml', version="v9")
    
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


class AuthenticationForm(FlaskForm):
    validators = [DataRequired()]
    client_id = StringField('Client ID', validators=validators)
    client_secret = StringField('Client Secret', validators=validators)
    refresh_token = StringField('Refresh Token', validators=validators)
    developer_token = StringField('Developer Token', validators=validators)
    mcc = StringField('MCC ID', validators=validators)
    submit = SubmitField('Set Credentials')


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=int(os.environ.get("PORT", 8080)))