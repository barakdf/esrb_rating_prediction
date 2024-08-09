import requests
import pandas as pd
import time

# Define constants
STEAM_APP_LIST_URL = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json"
APP_DETAILS_URL = "http://store.steampowered.com/api/appdetails?appids={}"
TARGET_ESRB_RATINGS = ["m", "e", "t"]
NUM_GAMES_PER_RATING = 1  # Adjust this if you want a different distribution

# Fetch the list of apps
response = requests.get(STEAM_APP_LIST_URL)
app_list = response.json()['applist']['apps']

# Prepare a list to store our selected games
games = {
    "m": [],
    "e": [],
    "t": []
}

# Iterate over the list of apps and fetch details for each game
for app in app_list:
    appid = app['appid']
    try:
        # Fetch the game details
        details_response = requests.get(APP_DETAILS_URL.format(appid))
        if details_response.status_code != 200:
            print(f"Failed to fetch details for appid {appid}: HTTP {details_response.status_code}")
            continue

        details = details_response.json().get(str(appid), {}).get('data', {})
        print("Processing appid", appid)
        # Check if the 'details' is not None and is a dictionary
        if not isinstance(details, dict):
            print(f"Invalid details for appid {appid}: Data is not a dictionary.")
            continue

        # Check if the app is a game and has the desired ESRB rating
        if details.get('type') == 'game':
            print("Game found:", details.get('name', 'N/A'))
            esrb_rating = details.get('ratings', {}).get('esrb', {}).get('rating', "").lower()
            if esrb_rating in TARGET_ESRB_RATINGS and len(games[esrb_rating]) < NUM_GAMES_PER_RATING:
                # Save the relevant data
                game_data = {
                    "steam_appid": appid,
                    "name": details.get('name', ''),
                    "about_the_game": details.get('about_the_game', ''),
                    "esrb_rating": esrb_rating
                }
                games[esrb_rating].append(game_data)
                print(f"Added {esrb_rating.upper()} game: {game_data['name']}")

        # Stop if we have enough games for each rating
        if all(len(games[rating]) >= NUM_GAMES_PER_RATING for rating in TARGET_ESRB_RATINGS):
            break

    except Exception as e:
        print(f"Failed to process appid {appid}: {e}")

    # Be polite to the API and avoid rate limiting
    time.sleep(0.2)

# Combine the lists into a single DataFrame
all_games = games['m'] + games['e'] + games['t']
df = pd.DataFrame(all_games)

# Save to CSV
df.to_csv("steam_games.csv", index=False)
print("Data saved to steam_games.csv")
