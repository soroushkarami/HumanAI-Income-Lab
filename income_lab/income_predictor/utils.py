from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
dataset_path = BASE_DIR/'Trained Model'/'adult.csv'

def person_picker():
    df = pd.read_csv(dataset_path)

    person = df.sample(1)   # Pick 1 random row from df; the row is a DataFrame

    person_features = person.iloc[0]    # convert the row from 'DataFrame' to a 'Series'
    person_income = person['income'].iloc[0]

    # -------------- for model to predict --------------
    for_model = person_features.drop(labels=['income']).to_dict()

    # -------------- for user to see --------------
    for_user = person_features.drop(labels=['income'])
    # modify columns for user:
    for_user_mdfy = modify_for_user(for_user)
    for_user_mdfy = for_user_mdfy.to_dict()
    for_user_ready = {
        k: v.replace('-', ' ') if isinstance(v, str) else v
        for k, v in for_user_mdfy.items()
    }

    return for_model, for_user_ready, person_income


def modify_for_user(user_features):
    """
        Cosmetic-only cleanup for UI display.
        Does NOT affect model features.
    """

    # Replace '?' values (display only)
    for col in user_features.index:
        if user_features[col] == '?':
            user_features[col] = 'Unknown'

    # Capital net (display only)
    user_features['Capital Net'] = (
            user_features['capital_gain'] - user_features['capital_loss']
    )

    # Drop technical columns from UI
    for col in ['fnlwgt', 'capital_gain', 'capital_loss', 'education_num']:
        user_features = user_features.drop(labels=col, errors='ignore')

    user_features.index = (user_features.index.str.replace('_', ' ').str.title())

    return user_features