import argparse
from time import time

import pandas as pd
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier


def evaluate_model(df):
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
