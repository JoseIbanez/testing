# pip install google-auth-oauthlib
import json
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials


# https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html

CLIENT_SECRET = 'gphoto_oauth.json'


def getRefreshToken():

    scopes_arr = [
        'https://www.googleapis.com/auth/photoslibrary',
        'https://www.googleapis.com/auth/photoslibrary.sharing'
        ]

    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET,
        scopes=scopes_arr)

    cred = flow.run_local_server(
        host='localhost',
        port=8088,
        authorization_prompt_message='Please visit this URL: {url}',
        success_message='The auth flow is complete; you may close this window.',
        open_browser=True)

    with open('refresh.token', 'w+') as f:
        f.write(cred._refresh_token)

    print('Refresh Token:', cred._refresh_token)
    print('Saved Refresh Token to file: refresh.token')



# This function creates a new Access Token using the Refresh Token
# and also refreshes the ID Token (see comment below).
def refreshToken():

    with open(CLIENT_SECRET, "r") as json_file:
        client_secret = json.load(json_file)

    with open('refresh.token', "r") as token_file:
        refresh_token = token_file.read()


    params = {
        "grant_type": "refresh_token",
        "client_id": client_secret["installed"]["client_id"],
        "client_secret": client_secret["installed"]["client_secret"],
        "refresh_token": refresh_token
    }

    authorization_url = "https://www.googleapis.com/oauth2/v4/token"

    r = requests.post(authorization_url, data=params)

    if r.ok:
        #print(f"accessToken: {r.json()['access_token']}")
        return r.json()['access_token']
    else:
        return None

# Call refreshToken which creates a new Access Token
#ret = getRefreshToken()
access_token = refreshToken()

# Pass the new Access Token to Credentials() to create new credentials
credentials = Credentials(access_token)
print(credentials)

