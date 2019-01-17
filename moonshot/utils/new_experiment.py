# The data set used in this example is from http://archive.ics.uci.edu/ml/datasets/Wine+Quality
# P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
# Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.

import os
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet

import mlflow.sklearn
from mlflow.tracking import MlflowClient


if __name__ == "__main__":

    client = MlflowClient(tracking_uri="databricks")
    # client.create_experiment("Moonshot S3", "s3://reservoir.truex.com/users/shuyang/mlflow/moonshot")
    client.restore_experiment(experiment_id=1)
