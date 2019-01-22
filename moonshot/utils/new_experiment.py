from mlflow.tracking import MlflowClient


if __name__ == "__main__":

    client = MlflowClient(tracking_uri="databricks")
    client.create_experiment("Moonshot S3", "s3://reservoir.truex.com/users/shuyang/mlflow/moonshot")
    client.restore_experiment(experiment_id=1)
