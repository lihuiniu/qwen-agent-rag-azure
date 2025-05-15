from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import CommandJob

def trigger_retrain_job():
    ml_client = MLClient(
        DefaultAzureCredential(),
        subscription_id="your-sub-id",
        resource_group_name="your-rg",
        workspace_name="your-ws"
    )
    job = CommandJob(
        code="./app", command="python train.py",
        environment="AzureML-sklearn:1", compute="cpu-cluster"
    )
    ml_client.jobs.create_or_update(job)
