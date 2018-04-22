from scipy.stats import randint as sp_randint
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from time import time
import argparse
import numpy as np
import pandas as pd


def _report(results, n_top=3):
    # Utility function to report best scores
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}\n".format(results['params'][candidate]))


def evaluate_model(file_name):
    df = pd.read_csv(file_name, sep=';')
    df = df[[i for i in list(df.columns) if i not in ('Unnamed: 0')]]
    df = df.fillna(value=0.0)
    rf = RandomForestClassifier(n_jobs=-1, n_estimators=200)
    folded_data = model_selection.KFold(n_splits=5)

    dfX = df[[i for i in list(df.columns) if i not in ('is_target')]]
    dfY = df['is_target']

    scores = []
    for k, (train, test) in enumerate(folded_data.split(dfX, dfY)):
        rf.fit(dfX.iloc[train].dropna(), dfY.iloc[train])
        score = rf.score(dfX.iloc[test], dfY.iloc[test])
        scores.append(score)
        print('[fold {0}], score: {1:.3f}'.format(k, score))

    # Randomized search of best params combination
    param_dist = {"max_depth": np.array(np.arange(3, 22, 3)),
                  "max_features": sp_randint(1, 11),
                  "min_samples_split": sp_randint(2, 11),
                  "min_samples_leaf": sp_randint(1, 11),
                  "bootstrap": [True, False],
                  "criterion": ["gini", "entropy"]}

    # run randomized search
    n_iter_search = 20
    random_search = RandomizedSearchCV(
        rf, param_distributions=param_dist,
        n_iter=n_iter_search, n_jobs=-1
    )
    start = time()
    random_search.fit(dfX, dfY)
    print("RandomizedSearchCV took %.2f seconds for %d candidates"
          " parameter settings." % ((time() - start), n_iter_search))
    _report(random_search.cv_results_)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Applies RandomForestClassifier to dataset',
        usage='python3 evaluate_model.py -dataset_csv ./12345.csv',
    )
    parser.add_argument(
        '-dataset_csv',
        dest='dataset_csv',
        help='Name of data set file',
        required=True,
    )
    args = parser.parse_args()
    evaluate_model(args.dataset_csv)
