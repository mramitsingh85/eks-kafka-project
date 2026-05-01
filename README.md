# 🚀 Kafka-Based Event-Driven Platform on AWS (EKS + MSK + GitOps)

---

# 📌 Overview

This project demonstrates a **production-grade event-driven architecture** using Kafka, deployed on Kubernetes with full CI/CD, observability, and autoscaling.

---

# 🧱 Architecture

```text
Client/App
   ↓
Producer (EKS)
   ↓
Kafka (AWS MSK - Multi Broker)
   ↓
Consumer Group (EKS - Scalable)
   ↓
Processing Layer

CI/CD: GitHub → Actions → ECR → ArgoCD → EKS
Monitoring: Prometheus → Grafana
Autoscaling: KEDA (Kafka Lag)
```

---

# ⚙️ Components

## Kafka (MSK)

* Multi-broker cluster
* Topic: `posts`
* Partitions: 3
* Replication: 2

## Kubernetes (EKS)

* Runs producer and consumer
* Multi-node cluster
* Highly scalable

## CI/CD

* GitHub Actions builds images
* Push to ECR
* ArgoCD auto-deploys

## Monitoring

* Prometheus collects metrics
* Grafana dashboards visualize system

## Autoscaling

* KEDA scales consumers based on Kafka lag

---

# 📂 Project Structure

```text
.
├── app
│   ├── consumer
│   │   ├── consumer.py
│   │   └── Dockerfile
│   └── producer
│       ├── Dockerfile
│       └── producer.py
├── helm
│   └── kafka-app
│       ├── Chart.yaml
│       ├── templates
│       │   ├── consumer.yaml
│       │   └── producer.yaml
│       ├── values-dev.yaml
│       ├── values-prod.yaml
│       └── values.yaml
├── k8s
│   ├── consumer.yaml
│   └── producer.yaml
├── kafka-exporter-values.yaml
├── README.md
└── terraform
    ├── eks.tf
    ├── main.tf
    ├── msk.tf
    ├── outputs.tf
    ├── provider.tf
    ├── terraform.tfstate
    ├── terraform.tfstate.backup
    ├── variables.tf
    └── vpc.tf
```

---

# 🧠 Design Principles

* Microservices architecture
* GitOps deployment
* Infrastructure as Code
* Observability-first design
* Event-driven scaling

---

# 🚀 Setup Steps

## 1. Provision Infra

```bash
cd terraform
terraform init
terraform apply
```

---

## 2. Build & Push Images

```bash
docker build -t producer ./app/producer
docker build -t consumer ./app/consumer

docker tag producer <ECR>/producer:latest
docker tag consumer <ECR>/consumer:latest

docker push <ECR>/producer:latest
docker push <ECR>/consumer:latest
```

---

## 3. Deploy via ArgoCD

```bash
kubectl apply -f argocd-app.yaml
```

---

## 4. Monitoring Setup

```bash
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace
```

---

## 5. Kafka Exporter

```bash
helm install kafka-exporter prometheus-community/prometheus-kafka-exporter \
  -f kafka-exporter-values.yaml \
  --namespace monitoring
```

---

## 6. KEDA

```bash
helm install keda kedacore/keda \
  --namespace keda --create-namespace
```

---

# 🧪 Local Development

```bash
docker-compose up -d
```

Includes Kafka + UI for testing.

---

# 📊 Observability

## Grafana

```bash
kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80
```

---

## Prometheus

```bash
kubectl port-forward svc/monitoring-kube-prometheus-prometheus -n monitoring 9091:9090
```

---

# ⚠️ Challenges & Solutions

## Kafka Timeout

* Cause: Security group
* Fix: Open port 9094

## Helm Error

* Cause: invalid parsing
* Fix: use values.yaml

## Pods Pending (Resources)

* Fix: scale node group

## Pods Pending (Too many pods)

* Cause: ENI limit
* Fix: increase nodes

## Image Not Updating

* Fix: imagePullPolicy: Always

---

# 🔧 Production Hardening & Fixes

## 1. Image Pull Fix

```yaml
imagePullPolicy: Always
```

---

## 2. Image Versioning

Use commit-based tagging instead of `latest`.

---

## 3. Resource Limits

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "300m"
    memory: "256Mi"
```

---

## 4. Terraform Backend

```hcl
backend "s3" {
  bucket = "eks-kafka-terraform-state"
  key    = "terraform.tfstate"
}
```

---

## 5. Alerting

* Kafka lag alerts
* Pod failure alerts

---

## 6. Security

* Replace AWS keys with IAM roles (OIDC)

---

## 7. Health Checks

```yaml
livenessProbe
readinessProbe
```

---

## 8. Scaling Fix (Real Issue)

Problem:

```
Too many pods
```

Solution:

* Increased node count to 5
* Learned EKS pod density limits

---

## 9. Git Ignore

```text
*.tfstate
*.tfstate.backup
```

---

# 📈 Scaling Strategy

* Kafka partitions → parallelism
* Kubernetes → scaling pods
* KEDA → event-driven scaling

---

# 🎯 Interview Q&A

## How does it scale?

Kafka partitions + KEDA autoscaling

## What is Kafka lag?

Difference between produced and consumed messages

## Biggest challenge?

Pod scheduling due to ENI limits

## Why ArgoCD?

GitOps automation

## High availability?

Kafka replication + multi-node EKS

---

# 🧾 Summary

Built a scalable, fault-tolerant Kafka system using:

* AWS MSK
* EKS
* Helm + ArgoCD
* GitHub Actions
* Prometheus + Grafana
* KEDA autoscaling

Handled real-world issues like pod density limits and deployment reliability.
