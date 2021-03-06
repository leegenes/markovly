from requests_oauthlib import OAuth2Session
import os, requests

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

class Auth:
    def __init__(   self,
                    client_id,
                    client_secret,
                    redirect_uri,
                    scope=[]):

        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.redirect_uri = redirect_uri
        self.access_token = '' 
        self.refresh_token = os.environ['SPOTIFY_REFRESH_TOKEN']
        self.oauth = self.auth_session()
    
    def auth_session(self):
        if not self.refresh_token:
            oauth = OAuth2Session(self.client_id,
                                redirect_uri=self.redirect_uri,
                                scope=self.scope)
            auth_url, state = oauth.authorization_url(AUTH_URL)
            print('Go to: ' + auth_url)
            auth_response = input('Enter full redirected URL: ')
            token = oauth.fetch_token(TOKEN_URL,
                                    authorization_response=auth_response,
                                    client_secret=self.client_secret)
            self.update_tokens(token['access_token'], refresh=token['refresh_token'])
        else:
            r = requests.request('POST',
                    TOKEN_URL,
                    auth=(self.client_id, self.client_secret),
                    data={'grant_type': 'refresh_token',
                        'refresh_token': self.refresh_token})
            token = r.json()
            self.update_tokens(token['access_token'])

    def set_refresh_config_var(self, refresh_token):
        heroku_key = os.environ['MY_HEROKU_API_KEY']
        r = requests.request('PATCH',
            'https://api.heroku.com/apps/peaceful-cliffs-64323/config-vars',
            json={'SPOTIFY_REFRESH_TOKEN': refresh_token},
            headers={'Content-Type': 'application/json',
                    'Accept': 'application/vnd.heroku+json; version=3',
                    'Authorization': 'Bearer {}'.format(heroku_key)}
                    )

    def update_tokens(self, access, refresh=None): 
        if refresh:
            self.refresh_token = refresh
            self.set_refresh_config_var(refresh)

        self.access_token = access 
