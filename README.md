# pimonitor

A simple python application to send heartbeat metrics to AWS CloudWatch.

## Docker Build

- To build the docker image run:

```bash
$ docker build . \
-t <your-docker-registry>/pimonitor:latest \
--platform linux/arm64
```

- Push the image to your docker registry:

```bash
$ docker push <your-docker-registry>/pimonitor:latest
```

# Kubernetes Deployment

- Create the namespace

```bash
$ kubectl create -f k8s/namespace.yml
```

- Create the secret

```bash
$ kubectl create secret generic cloudwatch \
--from-literal=aws_access_key_id=<your-aws-access-key-id> \
--from-literal=aws_secret_access_key=<your-aws-secret-access-key> \
--namespace=monitoring
```

- Create the deployment

```bash
$ kubectl apply -f k8s/deployment.yml \
--namespace monitoring
```
