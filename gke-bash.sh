#!/bin/bash

set -e

# Variables
PROJECT_ID="ljawn-se-lab"
ZONE="asia-southeast1-a"

# Decode and save the service account keyz
#echo "$GOOGLE_APPLICATION_CREDENTIALS_JSON" | base64 --decode > ${HOME}/gcloud-service-key.json

# Authenticate to GCP
#gcloud auth activate-service-account --key-file=${HOME}/gcloud-service-key.json

gcloud config set project $PROJECT_ID
gcloud config set compute/zone $ZONE
#gcloud services enable serviceusage.googleapis.com
#gcloud services enable container.googleapis.com
#gcloud services enable compute.googleapis.com

gcloud compute networks create jl-gke-vpc --subnet-mode=custom

gcloud compute networks subnets create my-subnet-asia-southeast1-a \
    --network=jl-gke-vpc \
    --region=asia-southeast1 \
    --range=10.0.0.0/24

gcloud compute networks subnets create my-subnet-asia-southeast1-b \
    --network=jl-gke-vpc \
    --region=asia-southeast1 \
    --range=10.0.1.0/24

gcloud compute instances create jumphost \
    --project=ljawn-se-lab \
    --zone=asia-southeast1-a \
    --machine-type=e2-medium \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=my-subnet-asia-southeast1-a \
    --tags=jumphost \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --service-account=jl-gks-sa@ljawn-se-lab.iam.gserviceaccount.com

JUMPHOST_IP=$(gcloud compute instances describe jumphost \
    --zone=asia-southeast1-a \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

gcloud container clusters create jl-gke-sg \
    --enable-ip-alias \
    --network=jl-gke-vpc \
    --subnetwork=my-subnet-asia-southeast1-a \
    --enable-private-nodes \
    --master-ipv4-cidr=172.16.0.0/28 \
    --zone=asia-southeast1-a \
    --node-locations=asia-southeast1-a,asia-southeast1-b \
    --num-nodes=2 \
    --enable-master-authorized-networks \
    --master-authorized-networks=${JUMPHOST_IP}/32

gcloud compute routers create nat-router \
    --network=jl-gke-vpc \
    --region=asia-southeast1

gcloud compute routers nats create nat-config \
    --router=nat-router \
    --auto-allocate-nat-external-ips \
    --nat-all-subnet-ip-ranges \
    --region=asia-southeast1

gcloud compute firewall-rules create allow-ssh-from-external \
    --network=jl-gke-vpc \
    --allow=tcp:22 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=jumphost

gcloud compute firewall-rules create allow-internal-communication \
    --network=jl-gke-vpc \
    --allow=all \
    --source-ranges=10.0.0.0/16

