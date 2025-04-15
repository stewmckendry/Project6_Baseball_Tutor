#!/bin/bash
set -e
set -x

# dev-push.sh - Build and push the image for Baseball Tutor (local dev use)

ACR_NAME="aiappsregistry"
IMAGE_NAME="baseball-tutor"
IMAGE_TAG="dev"
FULL_TAG="$ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG"

echo "🔧 Building image: $FULL_TAG"
docker build -t "$FULL_TAG" .

echo "🔐 Logging in to ACR: $ACR_NAME"
az acr login --name "$ACR_NAME"

echo "📤 Pushing image to ACR..."
docker push "$FULL_TAG"

echo "✅ Done! Image pushed as: $FULL_TAG"
