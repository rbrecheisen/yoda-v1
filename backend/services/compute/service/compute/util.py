import pandas as pd


# ----------------------------------------------------------------------------------------------------------------------
def load_features(file_path, **kwargs):
    features = pd.read_csv(file_path, **kwargs)
    return features


# ----------------------------------------------------------------------------------------------------------------------
def load_features_for(file_path, target_column, values, **kwargs):
    features = load_features(file_path, **kwargs)
    tmp = []
    for i in range(len(values)):
        tmp.append(features[features[target_column] == values[i]])
    return pd.concat(tmp)


# ----------------------------------------------------------------------------------------------------------------------
def get_xy(features, target_column=None, exclude_columns=list()):
    predictors = list(features.columns)
    for column in exclude_columns:
        if column in predictors:
            predictors.remove(column)
    if target_column:
        if target_column not in exclude_columns:
            if target_column in predictors:
                predictors.remove(target_column)
    X = features[predictors]
    X = X.as_matrix()
    if target_column:
        y = features[target_column]
        y = y.as_matrix()
    else:
        y = None
    return X, y
