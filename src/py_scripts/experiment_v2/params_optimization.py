import argparse
from time import time

import numpy as np
import pandas as pd
from scipy.stats import randint as sp_randint
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV


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


def params_optimization(df):
    print('Starting params_optimization')
    dfX = df[[i for i in list(df.columns) if i not in ('is_target')]]
    dfY = df['is_target']
    rf = RandomForestClassifier(n_jobs=-1, n_estimators=200)
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
    print("RandomizedSearchCV took {0:.2f} seconds for {1} candidates"
          " parameter settings.".format((time() - start), n_iter_search))
    _report(random_search.cv_results_)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Applies RandomForestClassifier to dataset',
        usage='python3 params_optimization.py -dataset ./ml_dataset.csv',
    )
    parser.add_argument(
        '-dataset',
        dest='dataset',
        help='Name of data set file',
        required=True,
    )
    args = parser.parse_args()
    df = pd.read_csv(args.dataset, sep=';')
    df = df[[i for i in list(df.columns) if i not in ('Unnamed: 0')]]
    df = df.fillna(value=0.0)
    params_optimization(df)
