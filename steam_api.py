import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace with your Steam Web API key
api_key = os.getenv('STEAM_API_KEY')

BASE_URL = "http://api.steampowered.com"
STORE_URL = "http://store.steampowered.com"
IStoreService_URL = "https://api.steampowered.com/IStoreService"


def get_app_list(max_results=100000, include_games=True, include_dlc=False, include_software=False,
                 include_videos=False, include_hardware=False, last_appid=0):
    """
    Retrieves a list of all Steam applications with optional filters.

    Args:
        max_results (int): Number of results to return at a time. Default is 10,000, max is 50,000.
        include_games (bool): Include games in the results.
        include_dlc (bool): Include DLC in the results.
        include_software (bool): Include software items in the results.
        include_videos (bool): Include videos and series in the results.
        include_hardware (bool): Include hardware in the results.
        last_appid (int): For continuations, the last appid returned from the previous call.

    Returns:
        list: A list of dictionaries containing app ID, name, last modified, and price change number.
    """
    params = {
        'key': api_key,
        'max_results': max_results,
        'include_games': include_games,
        'include_dlc': include_dlc,
        'include_software': include_software,
        'include_videos': include_videos,
        'include_hardware': include_hardware,
        'last_appid': last_appid
    }

    url = f"{IStoreService_URL}/GetAppList/v1/"
    response = requests.get(url, params=params)
    if response.status_code == 200:
        response_data = response.json()['response']
        apps = response_data['apps']
        have_more_results = response_data.get('have_more_results', False)
        last_appid = response_data.get('last_appid', None)
        return apps, have_more_results, last_appid
    else:
        response.raise_for_status()


def get_all_apps():
    """
    Retrieves all Steam applications, handling pagination.

    Returns:
        list: A list of dictionaries containing all app details.
    """
    all_apps = []
    have_more_results = True
    last_appid = 0

    while have_more_results:
        apps, have_more_results, last_appid = get_app_list(last_appid=last_appid)
        all_apps.extend(apps)

    return all_apps


def get_app_details(app_id):
    """
    Retrieves detailed information about a specific Steam application.

    Args:
        app_id (int): The application ID to retrieve details for.

    Returns:
        dict: A dictionary containing detailed information about the application.
    """
    url = f"{STORE_URL}/api/appdetails?appids={app_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data[str(app_id)]['success']:
            return data[str(app_id)]['data']
    else:
        response.raise_for_status()


def collect_game_data(app_ids):
    """
    Collects game data for a list of application IDs.

    Args:
        app_ids (list): A list of application IDs to retrieve data for.

    Returns:
        list: A list of dictionaries containing game data.
    """
    game_details = []
    for app_id in app_ids:
        details = get_app_details(app_id)
        if details:
            game_data = {
                'app_id': app_id,
                'name': details.get('name', 'N/A'),
                'required_age': details.get('required_age', 'N/A'),
                'is_free': details.get('is_free', 'N/A'),
                'controller_support': details.get('controller_support', 'N/A'),
                'detailed_description': details.get('detailed_description', 'N/A'),
                'about_the_game': details.get('about_the_game', 'N/A'),
                'short_description': details.get('short_description', 'N/A'),
                'supported_languages': details.get('supported_languages', 'N/A'),
                'header_image': details.get('header_image', 'N/A'),
                'website': details.get('website', 'N/A'),
                'developers': ', '.join(details.get('developers', [])),
                'publishers': ', '.join(details.get('publishers', [])),
                'platforms': details.get('platforms', {}),
                'categories': ', '.join([cat.get('description', 'N/A') for cat in details.get('categories', [])]),
                'genres': ', '.join([genre.get('description', 'N/A') for genre in details.get('genres', [])]),
                'screenshots': [screenshot.get('path_full', 'N/A') for screenshot in details.get('screenshots', [])],
                'movies': [movie.get('webm', {}).get('max', 'N/A') for movie in details.get('movies', [])],
                'release_date': details.get('release_date', {}).get('date', 'N/A'),
                'support_info': details.get('support_info', {}),
                'background': details.get('background', 'N/A'),
                'content_descriptors': details.get('content_descriptors', {}),
                'ratings': details.get('ratings', {}),
            }
            game_details.append(game_data)
    return game_details



