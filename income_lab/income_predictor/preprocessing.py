from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


class AdultPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.country_freq = None
        self.mode_country = None

    def fit(self, X, y=None):
        df = X.copy()

        # Replace '?' everywhere
        df.replace('?', np.nan, inplace=True)
        cols_except_country = [c for c in df.columns if c != 'native_country']
        df.dropna(subset=cols_except_country, inplace=True)

        self.mode_country = df['native_country'].mode()[0]

        # country frequency mapping
        counts = df['native_country'].value_counts()
        self.country_freq = counts.to_dict()

        return self


    def transform(self, X):
        df = X.copy()

        df.replace('?', np.nan, inplace=True)
        df['native_country'] = df['native_country'].fillna(self.mode_country)

        # capital_net
        if 'capital_net' not in df.columns:
            if ('capital_gain' in df.columns) and ('capital_loss' in df.columns):
                df['capital_net'] = df['capital_gain'] - df['capital_loss']
            else:
                df['capital_net'] = 0

        # dropping unnecessary cols
        cols_to_drop = ['fnlwgt', 'education', 'capital_gain', 'capital_loss']
        df = df.drop(columns=[col for col in cols_to_drop if col in df.columns],
                     errors='ignore')

        # frequency encoding
        df['native_country'] = (
            df['native_country'].map(self.country_freq).fillna(0)
        )

        return df