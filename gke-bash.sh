#!/bin/bash

set -e

# Variables
PROJECT_ID="ljawn-se-lab"
CLUSTER_NAME="jl-gks"
ZONE="asia-southeast1-a" # Singapore region zone
NETWORK_NAME="jl-gks-vpc"
SUBNET_NAME="jl-gks-subnet"
SUBNET_RANGE="10.0.0.0/24"
NUM_NODES=1
FIREWALL_RULE_NAME="allow-internet-access"

# Decode and save the service account key
echo "$GOOGLE_APPLICATION_CREDENTIALS_JSON" | base64 --decode > ${HOME}/gcloud-service-key.json

# Authenticate to GCP
gcloud auth activate-service-account --key-file=${HOME}/gcloud-service-key.json

# Set the project
gcloud config set project $PROJECT_ID

# Create a VPC network
if ! gcloud compute networks describe $NETWORK_NAME >/dev/null 2>&1; then
  gcloud compute networks create $NETWORK_NAME --subnet-mode=custom
else
  echo "VPC network $NETWORK_NAME already exists."
fi

# Create a subnet in the VPC network
if ! gcloud compute networks subnets describe $SUBNET_NAME --region=$(echo $ZONE | sed 's/-[a-z]$//') >/dev/null 2>&1; then
  gcloud compute networks subnets create $SUBNET_NAME \
    --network=$NETWORK_NAME \
    --range=$SUBNET_RANGE \
    --region=$(echo $ZONE | sed 's/-[a-z]$//')
else
  echo "Subnet $SUBNET_NAME already exists."
fi

# Create a GKE cluster in the subnet
if ! gcloud container clusters describe $CLUSTER_NAME --zone $ZONE >/dev/null 2>&1; then
  gcloud container clusters create $CLUSTER_NAME \
    --zone $ZONE \
    --network $NETWORK_NAME \
    --subnetwork $SUBNET_NAME \ 
    --num-nodes $NUM_NODES
else
  echo "GKE cluster $CLUSTER_NAME already exists."
fi

# Create a firewall rule to allow internet accessz
if ! gcloud compute firewall-rules describe $FIREWALL_RULE_NAME >/dev/null 2>&1; then
  gcloud compute firewall-rules create $FIREWALL_RULE_NAME \
    --network $NETWORK_NAME \
    --allow tcp:80,tcp:443 \
    --source-ranges 0.0.0.0/0
else
  echo "Firewall rule $FIREWALL_RULE_NAME already exists."
fi

# Get credentials for kubectl
gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE

# Deploy a sample application
#kubectl create deployment hello-world --image=gcr.io/google-samples/hello-app:1.0

# Expose the deployment to the internet
#kubectl expose deployment hello-world --type=LoadBalancer --port 80 --target-port 8080

#echo "GKE cluster created and application exposed to the internet."
