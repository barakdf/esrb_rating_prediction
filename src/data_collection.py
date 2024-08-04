import pandas as pd
import os
from steam_api import get_all_apps, get_app_details
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import time
import sys

processed_data_dir = 'data/processed'
apps_list_file_path = 'data/all_apps.csv'
descriptions_file_path = 'data/game_descriptions.csv'


def load_esrb_datasets():
    print("Loading ESRB datasets...")
    train_esrb_df = pd.read_csv('data/train_esrb.csv')
    test_esrb_df = pd.read_csv('data/test_esrb.csv')
    return train_esrb_df, test_esrb_df


def save_all_apps_to_csv(all_apps):
    print("Saving all Steam apps to CSV file...")
    all_apps_df = pd.DataFrame(all_apps)
    all_apps_df.to_csv(apps_list_file_path, index=False)


def load_all_apps_from_csv():
    print("Loading all Steam apps from CSV file...")
    all_apps_df = pd.read_csv(apps_list_file_path)
    return all_apps_df.to_dict('records')


def create_title_to_app_id_mapping(all_apps):
    print("Creating title to app ID mapping...")
    return {app['name']: app['appid'] for app in all_apps}


def map_titles_to_app_ids(combined_esrb_df, title_to_app_id):
    print("Mapping titles to app IDs in the ESRB datasets...")
    combined_esrb_df['app_id'] = combined_esrb_df['title'].map(title_to_app_id)
    combined_esrb_df['app_id'] = combined_esrb_df['app_id'].astype(pd.Int64Dtype())
    return combined_esrb_df


def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.get_text(separator=' ')


def get_game_descriptions(app_ids, delay=1, retries=3):
    descriptions = []
    total_apps = len(app_ids)
    for idx, app_id in enumerate(app_ids):
        if pd.notna(app_id):
            success = False
            for attempt in range(retries):
                try:
                    sys.stdout.write(f"\rFetching details for app_id {app_id} ({idx + 1}/{total_apps})...")
                    sys.stdout.flush()
                    details = get_app_details(int(app_id))
                    if details:
                        cleaned_description = clean_html(details.get('short_description', 'N/A'))
                        descriptions.append({
                            'app_id': app_id,
                            'title': details.get('name', 'N/A'),
                            'description': cleaned_description
                        })
                    success = True
                    break
                except HTTPError as e:
                    print()
                    if e.response.status_code == 429:
                        print(f"Rate limit hit for app_id {app_id}. Retrying after delay ({attempt + 1}/{retries})...")
                        time.sleep(delay)
                    else:
                        print(f"HTTPError for app_id {app_id}: {e}")
                        break
            if not success:
                print(f"Failed to fetch details for app_id {app_id} after {retries} retries.")
    print()
    return descriptions


def save_descriptions_to_csv(descriptions_df, descriptions_file_path):
    print("Saving game descriptions to CSV file...")
    descriptions_df.to_csv(descriptions_file_path, index=False)


def merge_descriptions_with_esrb_datasets(train_esrb_df, test_esrb_df, descriptions_df):
    print("Merging descriptions with ESRB datasets...")
    train_merged_df = train_esrb_df.merge(descriptions_df, on='title', how='inner')
    test_merged_df = test_esrb_df.merge(descriptions_df, on='title', how='inner')
    return train_merged_df, test_merged_df


def select_and_rename_columns(train_merged_df, test_merged_df):
    print("Selecting and renaming relevant columns for description-based datasets...")
    train_description_based_df = train_merged_df[['title', 'description', 'esrb_rating']]
    test_description_based_df = test_merged_df[['title', 'description', 'esrb_rating']]
    return train_description_based_df, test_description_based_df


def save_new_datasets(train_description_based_df, test_description_based_df, train_original_filtered_df,
                      test_original_filtered_df):
    print("Saving the new datasets...")
    train_description_based_df.to_csv(f'{processed_data_dir}/train_description_based_esrb_dataset.csv', index=False)
    test_description_based_df.to_csv(f'{processed_data_dir}/test_description_based_esrb_dataset.csv', index=False)
    train_original_filtered_df.to_csv(f'{processed_data_dir}/train_original_filtered_esrb_dataset.csv', index=False)
    test_original_filtered_df.to_csv(f'{processed_data_dir}/test_original_filtered_esrb_dataset.csv', index=False)
    print(f"Data collection complete. Data saved to {processed_data_dir}")


def main():
    train_esrb_df, test_esrb_df = load_esrb_datasets()
    combined_esrb_df = pd.concat([train_esrb_df, test_esrb_df])

    if os.path.exists(apps_list_file_path):
        all_apps = load_all_apps_from_csv()
    else:
        print("Fetching all Steam apps...")
        all_apps = get_all_apps()
        save_all_apps_to_csv(all_apps)

    title_to_app_id = create_title_to_app_id_mapping(all_apps)
    combined_esrb_df = map_titles_to_app_ids(combined_esrb_df, title_to_app_id)

    if os.path.exists(descriptions_file_path):
        print("Loading game descriptions from existing CSV file...")
        descriptions_df = pd.read_csv(descriptions_file_path)
    else:
        print("Fetching descriptions for all app IDs...")
        app_ids = combined_esrb_df['app_id'].dropna().unique().tolist()
        game_descriptions = get_game_descriptions(app_ids)
        descriptions_df = pd.DataFrame(game_descriptions)
        save_descriptions_to_csv(descriptions_df, descriptions_file_path)

    train_merged_df, test_merged_df = merge_descriptions_with_esrb_datasets(train_esrb_df, test_esrb_df,
                                                                            descriptions_df)
    train_description_based_df, test_description_based_df = select_and_rename_columns(train_merged_df, test_merged_df)

    train_original_filtered_df = train_merged_df.drop(columns=['console', 'description', 'app_id'])
    test_original_filtered_df = test_merged_df.drop(columns=['console', 'description', 'app_id'])

    os.makedirs(processed_data_dir, exist_ok=True)
    save_new_datasets(train_description_based_df, test_description_based_df, train_original_filtered_df,
                      test_original_filtered_df)

    verify_esrb_rating_distribution()



def verify_esrb_rating_distribution():
    # get all the files from the processed data directory
    # Load the new datasets
    train_description_based_df = pd.read_csv(f'{processed_data_dir}/train_description_based_esrb_dataset.csv')
    test_description_based_df = pd.read_csv(f'{processed_data_dir}/test_description_based_esrb_dataset.csv')
    train_original_filtered_df = pd.read_csv(f'{processed_data_dir}/train_original_filtered_esrb_dataset.csv')
    test_original_filtered_df = pd.read_csv(f'{processed_data_dir}/test_original_filtered_esrb_dataset.csv')

    original_rating_distribution_train = train_original_filtered_df['esrb_rating'].value_counts(normalize=True)
    new_rating_distribution_train = train_description_based_df['esrb_rating'].value_counts(normalize=True)

    original_rating_distribution_test = test_original_filtered_df['esrb_rating'].value_counts(normalize=True)
    new_rating_distribution_test = test_description_based_df['esrb_rating'].value_counts(normalize=True)

    # Verify the distribution of ESRB ratings
    print("Verifying the distribution of ESRB ratings...")

    print("\nOriginal Training Rating Distribution:")
    print(original_rating_distribution_train)

    print("\nNew Training Rating Distribution:")
    print(new_rating_distribution_train)

    print("\nOriginal Test Rating Distribution:")
    print(original_rating_distribution_test)

    print("\nNew Test Rating Distribution:")
    print(new_rating_distribution_test)


if __name__ == "__main__":
    # main()

    verify_esrb_rating_distribution()