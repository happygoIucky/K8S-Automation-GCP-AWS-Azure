#!/bin/bash

set -e

# Variables
PROJECT_ID="ljawn-se-lab"
CLUSTER_NAME="jl-gks"
ZONE="asia-southeast1-a" # Singapore region zone
NETWORK_NAME="jl-gks-vpc"
SUBNET_NAME="jl-gks-subnet"
FIREWALL_RULE_NAME="allow-internet-access"

# Decode and save the service account key
echo "$GOOGLE_APPLICATION_CREDENTIALS_JSON" | base64 --decode > ${HOME}/gcloud-service-key.json

# Authenticate to GCP
gcloud auth activate-service-account --key-file=${HOME}/gcloud-service-key.json

# Set the project
gcloud config set project $PROJECT_ID

# Delete the GKE cluster
if gcloud container clusters describe $CLUSTER_NAME --zone $ZONE >/dev/null 2>&1; then
  gcloud container clusters delete $CLUSTER_NAME --zone $ZONE --quiet
else
  echo "GKE cluster $CLUSTER_NAME does not exist."
fi

# Delete the firewall rule
if gcloud compute firewall-rules describe $FIREWALL_RULE_NAME >/dev/null 2>&1; then
  gcloud compute firewall-rules delete $FIREWALL_RULE_NAME --quiet
else
  echo "Firewall rule $FIREWALL_RULE_NAME does not exist."
fi

# Delete the subnet
if gcloud compute networks subnets describe $SUBNET_NAME --region=$(echo $ZONE | sed 's/-[a-z]$//') >/dev/null 2>&1; then
  gcloud compute networks subnets delete $SUBNET_NAME --region=$(echo $ZONE | sed 's/-[a-z]$//') --quiet
else
  echo "Subnet $SUBNET_NAME does not exist."
fi

# Delete the VPC network
if gcloud compute networks describe $NETWORK_NAME >/dev/null 2>&1; then
  gcloud compute networks delete $NETWORK_NAME --quiet
else
  echo "VPC network $NETWORK_NAME does not exist."
fi

echo "GKE cluster and resources destroyed successfully."
