import numpy as np
import pandas as pd
import os
import logging
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from pymfe.mfe import MFE

from .getTrainingScores import getTrainingScores
from .getTPRFPR import getTPRFPR

def generate_full_train_test_set(source_path: str, full_dest_path: str, train_dest_path: str,
                                 test_dest_path: str, scaling_method: str = None,
                                 test_size=0.5, random_state=42):
    assert scaling_method is None or scaling_method in ["minmax", "zscore"], "scaling_method must be None, 'minmax' or 'zscore'"
    
    scaler = None
    if scaling_method == "minmax":
        scaler = MinMaxScaler()
    elif scaling_method == "zscore":
        scaler = StandardScaler()

    dataset_list = [csv for csv in os.listdir(source_path) if csv.endswith(".csv")]

    if not os.path.exists(full_dest_path):
        os.makedirs(full_dest_path)

    if not os.path.exists(train_dest_path):
        os.makedirs(train_dest_path)
    
    if not os.path.exists(test_dest_path):
        os.makedirs(test_dest_path)
    
    for dataset_name in dataset_list:
        dataset = pd.read_csv(f"{source_path}/{dataset_name}")
        
        columns = dataset.columns
        y = dataset[columns[-1]].values
        X = dataset.drop(columns[-1], axis=1).values
        # y = dataset.pop(dataset.columns[-1])
        if scaler:
            X = scaler.fit_transform(X)
        # else:
        #     X = dataset.values
        X = np.c_[X, y]
        dataset_transformed = pd.DataFrame(data=X, columns=columns)

        train, test = train_test_split(dataset_transformed, test_size=test_size, random_state=random_state)

        dataset.to_csv(f"{full_dest_path}/{dataset_name}", index=False)
        # # # dataset_transformed.to_csv(f"{full_dest_path}/{dataset_name}", index=False)
        train.to_csv(f"{train_dest_path}/{dataset_name}", index=False)
        test.to_csv(f"{test_dest_path}/{dataset_name}", index=False)

def load_train_test_data(dataset_name: str, train_data_path: str, test_data_path: str):
    train_df = pd.read_csv(f"{train_data_path}/{dataset_name}.csv")
    y_train = train_df.pop(train_df.columns[-1])
    X_train = train_df

    test_df = pd.read_csv(f"{test_data_path}/{dataset_name}.csv")
    y_test = test_df.pop(test_df.columns[-1])
    X_test = test_df

    return X_train.to_numpy(), y_train.to_numpy(), X_test.to_numpy(), y_test.to_numpy()

def test_clf():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='clf_test.log', encoding='utf-8', level=logging.DEBUG)

    complete_data_path = "../data/datasets/"
    dataset_list = [csv for csv in os.listdir(complete_data_path) if csv.endswith(".csv")]
    
    scaler = StandardScaler()
    for i, dataset in enumerate(dataset_list):
        dataset_name = dataset.split(".csv")[0]

        df = pd.read_csv("../data/datasets/"+dataset)

        df_train, df_test = train_test_split(df, test_size=0.5, random_state=42)

        X_train = df_train.drop(columns=['class']).to_numpy()
        y_train = df_train['class'].to_numpy()

        X_train = scaler.fit_transform(X_train)

        clf = None
        clf = LogisticRegression(random_state=42, n_jobs=-1, max_iter=1000)
        
        calib_clf = CalibratedClassifierCV(clf, cv=3, n_jobs=-1)
        calib_clf.fit(X_train, y_train)

        scores = getTrainingScores(X_train, y_train, 10, clf)[0]
        tprfpr = getTPRFPR(scores)
        clf.fit(X_train, y_train)
           
        logger.info(f"Finished: {dataset}")

if __name__ == "__main__":
    # complete_data_path = "./data/datasets/"
    # dataset_list = [csv for csv in os.listdir(complete_data_path) if csv.endswith(".csv")]
    
    # for _, dataset in enumerate(dataset_list):
    #     df = pd.read_csv(complete_data_path + dataset)
    #     print(find_class(df))
    test_clf()