# pimonitor

A simple python application to send heartbeat metrics to AWS CloudWatch.

![Docker Container Actions Status](https://github.com/ssolkhon/pimonitor/actions/workflows/publish-docker-container.yml/badge.svg)

## Docker Build

When a commit is merged into the master branch a new docker image is built and
pushed to the docker registry. This can be found at:
`public.ecr.aws/ssolkhon/pimonitor:latest`

If you'd like to build the image yourself, follow the steps below:

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
$ kubectl create namespace monitoring
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

The supplied deployment file is also compatible with ArgoCD.
