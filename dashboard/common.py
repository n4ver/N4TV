import requests

def valid_url(url):
    if url.startswith("https://logs.tf/"):
        return True
    else:
        return False


def extract_log_no(url):
    lst = url.split("/")
    number = lst[-1].split("#")[0]
    try: int(number)
    except:
        return -1
    if int(number) <= 0:
        return -1
    return int(number)


def valid_log(url):
    return (valid_url(url) and extract_log_no(url) != -1)


def special_sort(lst):
    return sorted(lst, key = lambda x: x [1])


def get_steam_api_key():
    try:
        with open('STEAM_API.txt', 'r') as f:
            key = f.read()
    except FileNotFoundError:
        return None
    return key


def get_steam_user_info(STEAM_API_KEY, STEAMID64):
    base_url = r'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
    url = f'{base_url}?key={STEAM_API_KEY}&steamids={STEAMID64}&format=json'
    response = requests.get(url).json()
    return response

def get_steam_avatars(response):
    user = response['response']['players'][0]
    dct = {
        'small': user['avatar'],
        'medium': user['avatarmedium'],
        'large': user['avatarfull']
        }

    return dct

def commid_to_usteamid(commid):
    # Taken from https://gist.github.com/bcahue/4eae86ae1d10364bb66d
    usteamid = []
    usteamid.append('[U:1:')
    steamidacct = int(commid) - 76561197960265728 # magic number
    
    usteamid.append(str(steamidacct) + ']')
    
    return ''.join(usteamid)

def usteamid_to_commid(usteamid):
    # Taken from https://gist.github.com/bcahue/4eae86ae1d10364bb66d
    for ch in ['[', ']']:
        if ch in usteamid:
            usteamid = usteamid.replace(ch, '')
    
    usteamid_split = usteamid.split(':')
    commid = int(usteamid_split[2]) + 76561197960265728
  
    return commid