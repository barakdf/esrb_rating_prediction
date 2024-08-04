import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer


def preprocess_data(game_details_df):
    game_details_df = game_details_df[game_details_df['esrb_rating'] != 'N/A']
    le = LabelEncoder()
    game_details_df['genres'] = le.fit_transform(game_details_df['genres'].astype(str))
    game_details_df['categories'] = le.fit_transform(game_details_df['categories'].astype(str))

    vectorizer = TfidfVectorizer(max_features=1000)
    X_description = vectorizer.fit_transform(game_details_df['detailed_description'])

    X = pd.concat([game_details_df.drop(columns=['detailed_description', 'name', 'app_id', 'esrb_rating']),
                   pd.DataFrame(X_description.toarray())], axis=1)
    y = game_details_df['esrb_rating']
    return X, y
