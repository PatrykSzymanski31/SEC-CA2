from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
from functools import wraps
import os
import requests
import base64
import json

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

KEYCLOAK_INTERNAL_URL = os.getenv("KEYCLOAK_INTERNAL_URL")
KEYCLOAK_EXTERNAL_URL = os.getenv("KEYCLOAK_EXTERNAL_URL")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")

AUTH_URL = f"{KEYCLOAK_EXTERNAL_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth"
TOKEN_URL = f"{KEYCLOAK_INTERNAL_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
USERINFO_URL = f"{KEYCLOAK_INTERNAL_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/userinfo"
LOGOUT_URL = f"{KEYCLOAK_EXTERNAL_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/logout"

oauth = OAuth(app)
oauth.register(
    name="keycloak",
    client_id=KEYCLOAK_CLIENT_ID,
    client_secret=KEYCLOAK_CLIENT_SECRET,
    authorize_url=AUTH_URL,
    access_token_url=TOKEN_URL,
    client_kwargs={"scope": "openid profile email"},
)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = session.get("user")
        if not user:
            return redirect(url_for("login"))

        roles = user.get("roles", [])
        if "admin" not in roles:
            return "<h1>403 Forbidden</h1><p>You do not have the admin role.</p>", 403
        return f(*args, **kwargs)
    return decorated

@app.route("/")
def home():
    user = session.get("user")
    if user:
        return f"""
        <h1>Secure Cloud Lab</h1>
        <p>Logged in as: <strong>{user.get('preferred_username')}</strong></p>
        <p>Roles: {', '.join(user.get('roles', [])) or 'none'}</p>
        <p><a href='/backend'>Backend</a></p>
        <p><a href='/admin'>Admin page</a></p>
        <p><a href='/logout'>Logout</a></p>
        """
    return """
    <h1>Secure Cloud Lab</h1>
    <p>You are not logged in.</p>
    <p><a href='/login'>Login with Keycloak</a></p>
    """

@app.route("/login")
def login():
    redirect_uri = url_for("auth_callback", _external=True, _scheme="https")
    return oauth.keycloak.authorize_redirect(redirect_uri)

@app.route("/auth/callback")
def auth_callback():
    code = request.args.get("code")
    if not code:
        return "<h1>Error</h1><p>Missing authorization code.</p>", 400

    redirect_uri = url_for("auth_callback", _external=True, _scheme="https")

    token_response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": KEYCLOAK_CLIENT_ID,
            "client_secret": KEYCLOAK_CLIENT_SECRET,
        },
        timeout=10,
    )
    token_response.raise_for_status()
    token = token_response.json()

    userinfo_response = requests.get(
        USERINFO_URL,
        headers={"Authorization": f"Bearer {token['access_token']}"},
        timeout=10,
    )
    userinfo_response.raise_for_status()
    userinfo = userinfo_response.json()

    access_token = token.get("access_token", "")
    roles = []

    if access_token:
        try:
            parts = access_token.split(".")
            if len(parts) == 3:
                payload = parts[1]
                payload += "=" * (-len(payload) % 4)
                decoded = json.loads(base64.urlsafe_b64decode(payload).decode("utf-8"))
                roles = decoded.get("realm_access", {}).get("roles", [])
        except Exception:
           roles = []

    session["user"] = {
        "preferred_username": userinfo.get("preferred_username", "unknown"),
        "email": userinfo.get("email"),
        "roles": roles,
    }
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(f"https://127.0.0.1:8443/keycloak/realms/{KEYCLOAK_REALM}/protocol/openid-connect/logout")

@app.route("/backend")
@login_required
def backend():
    try:
        response = requests.get("http://internal-api:80", timeout=5)
        return f"<h1>Backend Response</h1><pre>{response.text}</pre>"
    except Exception as e:
        return f"<h1>Error reaching backend</h1><pre>{e}</pre>", 500

@app.route("/admin")
@admin_required
def admin():
    return "<h1>Admin page</h1><p>You have the admin role.</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

