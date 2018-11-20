import argparse
from time import time

import pandas as pd
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score


def evaluate_model(df):
    rf = RandomForestClassifier(n_jobs=-1, n_estimators=200, max_depth=5)
    params = {"max_depth": [5, 8, 11, 15, 20], "n_estimators": [100, 1000, 2000]}
    gr = GridSearchCV(rf, param_grid=params, n_jobs=6, cv=5,)
    folded_data = model_selection.KFold(n_splits=10)

    dfX = df[[i for i in list(df.columns) if i not in ('is_target')]]
    dfY = df['is_target']

    scores = []
    for k, (train, test) in enumerate(folded_data.split(dfX, dfY)):
        gr.fit(dfX.iloc[train].dropna(), dfY.iloc[train])
        score = gr.best_score_
        y_pred = gr.best_estimator_.predict(dfX.iloc[test])
        roc_auc_score(dfY.iloc[test], y_pred)
        scores.append(roc_auc_score)
        print('[fold {0}], score: {1:.3f}'.format(k, score))
    print('Mean: {0:.3f}'.format(sum(scores) / len(scores)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Applies RandomForestClassifier to dataset',
        usage='python3 evaluate_model.py -dataset ./ml_dataset.csv',
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
    start = time()
    evaluate_model(df)
    print('Execution time {0:.3f}'.format((time() - start)))
