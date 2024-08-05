#!/bin/bash

# Define your secrets from environment variables

# Add Helm repo
helm repo add grafana https://grafana.github.io/helm-charts

# Update Helm repo
helm repo update

# Install/Upgrade Helm release with provided values
helm upgrade --install --atomic --timeout 300s grafana-k8s-monitoring grafana/k8s-monitoring \
  --namespace "default" --create-namespace --values - <<EOF
cluster:
  name: jl-eks-sg
externalServices:
  prometheus:
    host: https://prometheus-prod-37-prod-ap-southeast-1.grafana.net
    basicAuth:
      username: "1700895"
      password: ${GRAFANA_TOKEN}
  loki:
    host: https://logs-prod-020.grafana.net
    basicAuth:
      username: "950355"
      password: ${GRAFANA_TOKEN}
  tempo:
    host: https://tempo-prod-14-prod-ap-southeast-1.grafana.net:443
    basicAuth:
      username: "944670"
      password: ${GRAFANA_TOKEN}
metrics:
  enabled: true
  cost:
    enabled: true
  node-exporter:
    enabled: true
logs:
  enabled: true
  pod_logs:
    enabled: true
  cluster_events:
    enabled: true
traces:
  enabled: true
receivers:
  grpc:
    enabled: true
  http:
    enabled: true
  zipkin:
    enabled: true
  grafanaCloudMetrics:
    enabled: false
opencost:
  enabled: true
  opencost:
    exporter:
      defaultClusterId: jl-eks-sg
    prometheus:
      external:
        url: https://prometheus-prod-37-prod-ap-southeast-1.grafana.net/api/prom
kube-state-metrics:
  enabled: true
prometheus-node-exporter:
  enabled: true
prometheus-operator-crds:
  enabled: true
alloy: {}
alloy-events: {}
alloy-logs: {}
EOF
