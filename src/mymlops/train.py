import joblib
import pandas as pd
from omegaconf import OmegaConf


def main():
    config = OmegaConf.load("./params.yaml")
    _train_inputs = joblib.load(config.features.train_features_save_path)
    _train_outputs = pd.read_csv(config.data.train_csv_save_path)
