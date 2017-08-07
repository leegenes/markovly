import spotipy, os, requests, re
import spotipy.util as sutil
from bs4 import BeautifulSoup, SoupStrainer

def spotipy_auth():
    scope = 'user-top-read'
    u = os.environ['SPOTIFY_USERNAME']
    token = sutil.prompt_for_user_token(u, scope)

    if token:
        s = spotipy.Spotify(token)
        return s

def get_top_tracks(auth):
    tracks = auth.current_user_top_tracks(limit=50, time_range='short_term')['items']
    return tracks

def search_for_lyrics(q):
    base_url = 'https://api.genius.com/search'
    payload = {'q': q}
    token = os.environ['GENIUS_ACCESS_TOKEN']
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.get(base_url,
                    headers=headers,
                    params=payload)
    hits = r.json()['response']['hits']
    num_to_compare = 10 if len(hits) >= 10 else len(hits)
    top_hits = hits[:num_to_compare]
    return top_hits 

def find_genius_match(name, artist, hits):
    for h in hits:
        if h['index'] == 'song':
            h_name = h['result']['title'].lower()
            h_artist = h['result']['primary_artist']['name'].lower()
            if h_name == name and h_artist == artist:
                return h
                break
    return False

def scrape_lyrics(url):
    r = requests.get(url)
    html = r.text
    strainer = SoupStrainer('div', 'lyrics')
    soup = BeautifulSoup(html, 'html.parser', parse_only=strainer).find('p')
#    for annotation in soup.find_all(['a', 'br']):
#        annotation.replaceWithChildren()
    soup = re.sub('(<(.*?)>|\[(.*?)\]|\(|\)|</br.+>)', '', soup.get_text())
    soup = soup.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')
    return soup 

def gather_lyrics():
    a = spotipy_auth()
    tracks = get_top_tracks(a)
    all_lyrics = ''
    for t in tracks:
        name = t['name'].lower()
        artist = t['artists'][0]['name'] .lower()
        query = name + ' ' + artist
        top_hits = search_for_lyrics(query)
        match = find_genius_match(name, artist, top_hits)
        if match:
            lyric_url = match['result']['url']
            lyrics = scrape_lyrics(lyric_url)
            all_lyrics += lyrics
    return all_lyrics

if __name__ == '__main__':
    gather_lyrics()
    
