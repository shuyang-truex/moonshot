from kubernetes import client, config


def create_service_object():
    svc = client.V1Service(
        kind="Service",
        api_version="v1",
        metadata=client.V1ObjectMeta(
            name="gateway-service",
            labels={"app": "gateway-service"}
        ),
        spec=client.V1ServiceSpec(
            selector={"app": "gateway"},
            ports=[client.V1ServicePort(protocol='TCP', port=8080, target_port=80, node_port=30000)],
            type="LoadBalancer"
        )
    )
    print(svc.to_str())
    return svc


def create_deployment_object(image):

    # Configureate Pod template container
    container = client.V1Container(
        name="gateway",
        image=image,
        ports=[client.V1ContainerPort(container_port=80)],
        command=["python", "gateway.py"],
        env=[client.V1EnvVar(name="NAME", value="gateway")]
    )

    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "gateway"}),
        spec=client.V1PodSpec(containers=[container]))

    # Create the specification of deployment
    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=1,
        template=template)

    # Instantiate the deployment object
    deployment = client.ExtensionsV1beta1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="gateway-deployment"),
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


def update_deployment(api_instance, deployment):
    # Update the deployment
    api_response = api_instance.patch_namespaced_deployment(
        name="gateway-deployment",
        namespace="default",
        body=deployment)
    print("Deployment updated. status='%s'" % str(api_response.status))


def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()
    extensions_v1beta1 = client.ExtensionsV1beta1Api()
    v1core = client.CoreV1Api()

    deployment = create_deployment_object(image="shengshuyang/gateway:0.0.6")
    service = create_service_object()

    # create_deployment(extensions_v1beta1, deployment)
    # create_service(v1core, service)
    update_deployment(extensions_v1beta1, deployment)


if __name__ == '__main__':
    main()
