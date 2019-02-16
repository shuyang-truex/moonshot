# moonshot
A demo of hosting moodring in kubernetes

## Useful Commands

Notes:

1. You don't need to mess with the `docker build/push` commands unless you wanna modify my images.
2. The yaml files under `deployments/`, `pods/` and `services/` are outdated and for referene only.
   The python code under `moonshot/serving` does exactly the same thing except that we can easily
   change input arguments and create multiple slightly different pods.
3. The code under `moonshot/training` trains a demo wine quality model and uploads it to our `mlflow`
   instance: https://truex.cloud.databricks.com/mlflow/, feel free to try that as well. I'd love to
   see `mlflow` gets integrated with our kubernetes cluster in the future.

```
// get started
brew install kubernetes-cli
brew cask install minikube
minikube start
minikube dashboard
minikube ip

# compile and push docker images
docker build -t shengshuyang/gateway:0.0.6 ./docker_images/gateway
docker push shengshuyang/gateway:0.0.6
docker build -t shengshuyang/xgboost-scorer:0.0.2 ./docker_images/xgboost
docker push shengshuyang/xgboost-scorer:0.0.2

# install python client https://github.com/kubernetes-client/python
pip install kubernetes

# add stuff to the kubernetes cluster
python moonshot/serving/deploy_model.py
python moonshot/serving/deploy_gateway.py

# cleanup
kubectl delete deployments --all
kubectl delete svc --all
kubectl delete pods --all
minikube stop

# commands for EKS (if so set up)
https://docs.aws.amazon.com/eks/latest/userguide/dashboard-tutorial.html
kubectl get services -o wide
http://afe11d559323311e9b0cb0ab75194da5-1194683322.us-east-1.elb.amazonaws.com:8080/?model_id=1&campaign_id=377
```
