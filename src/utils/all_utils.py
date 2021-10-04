import yaml
import os
import json

def read_yaml(path_to_yaml:str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    
    return content

def create_dirs(dirs: list):

    for dir in dirs:
        os.makedirs(dir, exist_ok=True)
        print(f"Directory is created at {dir}")

def save_data(data, path):

    data.to_csv(path, index=False )
    print(f"data saved at {path}")

def save_scores(scores, path, indentation=4):
    with open(path, "w") as f:
        json.dump(scores, f, indent=indentation)
    print(f"scores are saved at {path}")


