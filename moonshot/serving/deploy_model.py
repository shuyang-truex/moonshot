# Copyright 2016 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import path

import yaml

from kubernetes import client, config

DEPLOYMENT_NAME = "demo"


def create_service_object(model_id, campaign_id):
    svc = client.V1Service(
        kind="Service",
        api_version="v1",
        metadata=client.V1ObjectMeta(
            name="scoring-service-{}-{}".format(model_id, campaign_id),
            labels={"app": "scoring-service", "model_id": model_id, "campaign_id": campaign_id}
        ),
        spec=client.V1ServiceSpec(
            selector={"app": "xgboost", "model_id": model_id, "campaign_id": campaign_id},
            ports=[client.V1ServicePort(protocol='TCP', port=8080, target_port=80)],
            type="LoadBalancer"
        )
    )
    return svc


def create_deployment_object(image, model_id, campaign_id, model_path):

    deployment_name = "scoring-deployment-{}-{}".format(model_id, campaign_id)

    # Configureate Pod template container
    container = client.V1Container(
        name="xgboost-scorer",
        image=image,
        ports=[client.V1ContainerPort(container_port=80)],
        command=["python", "xgboost.py"],
        env=[client.V1EnvVar(name="NAME", value=deployment_name),
             client.V1EnvVar(name="MODEL_ID", value=model_id),
             client.V1EnvVar(name="CAMPAIGN_ID", value=campaign_id),
             client.V1EnvVar(name="MODEL_PATH", value=model_path)]
        )

    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "xgboost", "model_id": model_id, "campaign_id": campaign_id}),
        spec=client.V1PodSpec(containers=[container]))

    # Create the specification of deployment
    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=2,
        template=template,
        revision_history_limit=0)

    # Instantiate the deployment object
    deployment = client.ExtensionsV1beta1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=deployment_name),
        spec=spec)

    return deployment


def create_deployment(api_instance, deployment):
    # Create deployement
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace="default")
    print("Deployment created. status='%s'" % str(api_response.status))


def create_service(api_instance, service):
    # Create service
    api_response = api_instance.create_namespaced_service(
        body=service,
        namespace="default")
    print("Service created. status='%s'" % str(api_response.status))


def update_deployment(api_instance, deployment, model_id, campaign_id):
    # Update the deployment
    deployment_name = "scoring-deployment-{}-{}".format(model_id, campaign_id)
    api_response = api_instance.patch_namespaced_deployment(
        name=deployment_name,
        namespace="default",
        body=deployment)
    print("Deployment updated. status='%s'" % str(api_response.status))


def delete_deployment(api_instance):
    # Delete deployment
    api_response = api_instance.delete_namespaced_deployment(
        name=DEPLOYMENT_NAME,
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Deployment deleted. status='%s'" % str(api_response.status))


def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()
    extensions_v1beta1 = client.ExtensionsV1beta1Api()
    v1core = client.CoreV1Api()

    model_id, campaign_id, image = "1", "377", "shengshuyang/xgboost-scorer:0.0.4"
    # model_id, campaign_id, image = "2", "368", "shengshuyang/xgboost-scorer:0.0.4"

    deployment = create_deployment_object(
        image=image,
        model_id=model_id,
        campaign_id=campaign_id,
        model_path="s3://reservoir.truex.com/models/{}/{}".format(model_id, campaign_id)
    )
    service = create_service_object(model_id, campaign_id)

    # create_deployment(extensions_v1beta1, deployment)
    # create_service(v1core, service)

    update_deployment(extensions_v1beta1, deployment, model_id, campaign_id)

    # delete_deployment(extensions_v1beta1)


if __name__ == '__main__':
    main()
