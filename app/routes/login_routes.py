
from flask import Blueprint, request, url_for, redirect, session, jsonify
import json
from ..models.user import User, get_user
from app import db
from oauthlib.oauth2 import WebApplicationClient
import requests
import os
from flask_cors import CORS
from flask_wtf.csrf import generate_csrf


# Flask-Login helper to retrieve a user from our db


GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

root_bp = Blueprint("root_bp", __name__)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@root_bp.route("/", methods=["GET"])
def root():
    return {
        "name": "Mastermind API"
    }


@root_bp.route("/current", methods=["GET"])
def index():
    current_user = None
    if "google_uid" in session:
        current_user = get_user(session["google_uid"])

    if current_user:
        return current_user.to_json(), 200
    else:
        return {"name": None, "id": None}, 404


@root_bp.route("/login", methods=["GET"])
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@root_bp.route("/login/callback", methods=["GET"])
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    user = get_user(unique_id)
    response_code = 200
    if not user:
        user = User(google_uid=unique_id, name=users_name, email=users_email)
        db.session.add(user)
        db.session.commit()
        response_code = 201

    session["google_uid"] = user.google_uid

    # return user.to_json(), response_code

    return redirect(url_for("root_bp.index"))


@root_bp.route("/logout")
def logout():
    session["google_uid"] = None
    return {"success": "logged out"}
