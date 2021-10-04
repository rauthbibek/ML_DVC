import os
import argparse
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from src.utils.all_utils import read_yaml, create_dirs, save_scores
import joblib


def evaluate_metrics(actual_values, predicted_values):
    rmse = np.sqrt(mean_squared_error(actual_values, predicted_values))
    mae = mean_absolute_error(actual_values, predicted_values)
    r2 = r2_score(actual_values, predicted_values)

    return rmse, mae, r2

def evaluate(config_path, params_path):

    config = read_yaml(config_path)
    params = read_yaml(params_path)

    artifacts_dir = config["artifacts"]['artifacts_dir']
    split_data_dir = config["artifacts"]["split_data_dir"]
    test_file = config["artifacts"]["test_file"]
    test_data_path = os.path.join(artifacts_dir, split_data_dir, test_file)

    test = pd.read_csv(test_data_path)
    test_y = test["quality"]
    test_x = test.drop("quality", axis=1)

    model_dir = config["artifacts"]['model_dir']
    model_name = config["artifacts"]['model_name']
    
    model_dir_path = os.path.join(artifacts_dir, model_dir)
    model_path = os.path.join(model_dir_path, model_name)
    

    el = joblib.load(model_path)
    predicted_values = el.predict(test_x)
    rmse, mae, r2 = evaluate_metrics(test_y, predicted_values)
    scores={
        "rmse": rmse, "mae": mae, "r2":r2
    }
    score_dir = config["artifacts"]["scores_dir"]
    score_file = config["artifacts"]["score_file"]
    score_dir_path = os.path.join(artifacts_dir, score_dir)
    create_dirs([score_dir_path])
    score_file_path = os.path.join(score_dir_path, score_file)
    print(score_file_path)
    save_scores(scores, score_file_path)

if __name__ == '__main__':
    args = argparse.ArgumentParser()

    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")

    parsed_args = args.parse_args()

    evaluate(config_path=parsed_args.config, params_path=parsed_args.params)



