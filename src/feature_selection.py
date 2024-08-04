from sklearn.feature_selection import SelectKBest, chi2

def select_features(X, y, k=20):
    selector = SelectKBest(chi2, k=k)
    X_new = selector.fit_transform(X, y)
    return X_new
