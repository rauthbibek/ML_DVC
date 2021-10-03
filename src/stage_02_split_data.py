from os import read
from src.utils.all_utils import read_yaml, create_dirs, save_data
import argparse
import pandas as pd
import os
from sklearn.model_selection import train_test_split


def split_and_save(config_path, params_path):

    config = read_yaml(config_path)
    params = read_yaml(params_path)
    
    # split dataset(train & test) in the local directory
    # create path to directory: artifacts/split_data_dir/train.csv
    # create path to directory: artifacts/split_data_dir/test.csv
    artifacts_dir = config["artifacts"]['artifacts_dir']
    raw_local_dir = config["artifacts"]['raw_local_dir']
    raw_local_file = config["artifacts"]['raw_local_file']
    split_ratio = params["base"]["split_ratio"]
    random_state = params["base"]["random_state"]
    split_data_dir = config["artifacts"]["split_data_dir"]
    train_file = config["artifacts"]["train_file"]
    test_file = config["artifacts"]["test_file"]

    raw_local_file_path = os.path.join(artifacts_dir,raw_local_dir,raw_local_file)
    split_data_dir_path = os.path.join(artifacts_dir, split_data_dir)
    print(split_data_dir_path)
    create_dirs(dirs=[split_data_dir_path])

    train_data_path = os.path.join(artifacts_dir, split_data_dir, train_file)
    test_data_path = os.path.join(artifacts_dir, split_data_dir, test_file)

    df = pd.read_csv(raw_local_file_path)

    train, test = train_test_split(df, test_size= split_ratio, random_state= random_state)


    for data, path in (train, train_data_path), (test, test_data_path):
        save_data(data, path)


if __name__=='__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    split_and_save(config_path=parsed_args.config, params_path=parsed_args.params)

