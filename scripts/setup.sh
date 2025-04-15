#!/bin/bash
set -e
set -x  # 👈 this shows each command before it runs

# === CONFIGURATION ===
RESOURCE_GROUP="baseball-tutor-rg"
LOCATION="canadacentral"
PLAN_NAME="baseball-tutor-plan"
APP_NAME="baseball-ai-app"
ACR_NAME="aiappsregistry"              # ✅ Renamed from rfpevaluatoracr
IMAGE_NAME="baseball-tutor"
IMAGE_TAG="latest"
DOCKER_IMAGE="$ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG"

# === AZURE SETUP ===

echo "🛠️ Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

echo "🧱 Creating App Service plan..."
az appservice plan create \
  --name $PLAN_NAME \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux

echo "🌐 Creating Web App..."
# Ensure web app is created with proper container image and managed identity setup
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $PLAN_NAME \
  --name $APP_NAME \
  --deployment-container-image-name $DOCKER_IMAGE

echo "🔐 Granting ACR pull permission..."
# This assumes you're using system-assigned managed identity
az webapp identity assign --name $APP_NAME --resource-group $RESOURCE_GROUP

PRINCIPAL_ID=$(az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP --query identity.principalId --output tsv)
ACR_ID=$(az acr show --name $ACR_NAME --query id --output tsv)

az role assignment create --assignee $PRINCIPAL_ID \
  --scope $ACR_ID \
  --role AcrPull

echo "⚙️ Enabling managed identity credentials..."
az resource update \
  --ids $(az webapp show --name "$APP_NAME" --resource-group "$RESOURCE_GROUP" --query id --output tsv)/config/web \
  --set properties.acrUseManagedIdentityCreds=true

echo "⚙️ Setting container config..."
# Modern Azure CLI uses --container-image-name and --container-registry-url
az webapp config container set \
  --name "$APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --container-image-name "$DOCKER_IMAGE" \
  --container-registry-url "https://$ACR_NAME.azurecr.io"

echo "📦 Configuring environment variables..."
az webapp config appsettings set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings PORT=8000 OPENAI_API_KEY=$OPENAI_API_KEY

echo "🚀 All set! Use deploy.sh to build and push your image."
