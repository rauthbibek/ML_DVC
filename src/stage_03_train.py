import os
import argparse
import pandas as pd
from sklearn.linear_model import ElasticNet
from src.utils.all_utils import read_yaml, create_dirs

import joblib


def train(config_path, params_path):

    config = read_yaml(config_path)
    params = read_yaml(params_path)

    artifacts_dir = config["artifacts"]['artifacts_dir']
    split_data_dir = config["artifacts"]["split_data_dir"]
    train_file = config["artifacts"]["train_file"]
    train_data_path = os.path.join(artifacts_dir, split_data_dir, train_file)

    train = pd.read_csv(train_data_path)
    train_y = train["quality"]
    train_x = train.drop("quality", axis=1)

    model_dir = config["artifacts"]['model_dir']
    model_name = config["artifacts"]['model_name']
    
    model_dir_path = os.path.join(artifacts_dir, model_dir)
    model_path = os.path.join(model_dir_path, model_name)
    create_dirs([model_dir_path])

    alpha = params["model_params"]["ElasticNet"]["alpha"]
    l1_ratio = params["model_params"]["ElasticNet"]["l1_ratio"]
    random_state =  params["base"]["random_state"]

    el = ElasticNet(alpha=alpha, l1_ratio=l1_ratio,random_state=random_state)
    el.fit(train_x, train_y)

    joblib.dump(el, model_path)

if __name__ == '__main__':
    args = argparse.ArgumentParser()

    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")

    parsed_args = args.parse_args()

    train(config_path=parsed_args.config, params_path=parsed_args.params)



