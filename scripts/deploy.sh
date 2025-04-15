#!/bin/bash
set -e
set -x

################################################################################
# 🚀 DEPLOY.SH
#
# Deploy your RFP Evaluation App (FastAPI + Streamlit) to Azure App Service.
#
# 🔹 What it does:
#   - Builds the Docker image (unless --fast is used)
#   - Pushes the image to Azure Container Registry (ACR)
#   - Updates Azure App Service to use the new image
#   - Restarts the service and tails logs
#   - Runs a health check on the FastAPI /ping endpoint

# 🔸 How to run:
#   ./deploy.sh                   # Deploy, build new package with cache 
#   ./deploy.sh --fast            # Skip Docker build, just tag + deploy
#   ./deploy.sh --no-cache        # Clean rebuild of package before deploy
#
# 🔍 Logs & Debugging:
#   - Logs stream:   az webapp log tail --name rfp-ai-app --resource-group rfp-eval-rg
#   - Debug console: https://rfp-ai-app.scm.azurewebsites.net/DebugConsole
#   - Log files:     LogFiles/app/eval.log or LogFiles/default_docker.log
################################################################################

# === CONFIGURATION ===
RESOURCE_GROUP="baseball-tutor-rg"
LOCATION="canadacentral"
PLAN_NAME="baseball-tutor-plan"
APP_NAME="baseball-ai-app"
ACR_NAME="aiappsregistry"              # ✅ Renamed from rfpevaluatoracr
IMAGE_NAME="baseball-tutor"
DOCKERFILE="Dockerfile"
PING_URL="https://$APP_NAME.azurewebsites.net/health"

NO_CACHE_FLAG=""
SKIP_BUILD=false

# === PARSE CLI FLAGS ===
for arg in "$@"; do
  if [[ "$arg" == "--no-cache" || "$arg" == "--clean" ]]; then
    NO_CACHE_FLAG="--no-cache"
  elif [[ "$arg" == "--fast" ]]; then
    SKIP_BUILD=true
  fi
done

# === DETERMINE IMAGE TAG ===
if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  TAG=$(git rev-parse --short HEAD)
else
  TAG=$(date +%s)
fi
FULL_TAG="$ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG"

# === LOGIN TO ACR ===
echo "🔑 Logging into Azure Container Registry..."
az acr login --name "$ACR_NAME"

# === BUILD DOCKER IMAGE ===
# Ensure script is run from project root
if [ ! -f "$DOCKERFILE" ]; then
  echo "❌ Error: Dockerfile not found. Please run this script from the root of the project."
  exit 1
fi
if [ "$SKIP_BUILD" = false ]; then
  echo "🐳 Building image '$IMAGE_NAME' with tags: $FULL_TAG and latest $NO_CACHE_FLAG"
  docker buildx build \
    --platform linux/amd64 $NO_CACHE_FLAG \
    -f "$DOCKERFILE" \
    -t "$FULL_TAG" \
    -t "$ACR_NAME.azurecr.io/$IMAGE_NAME:latest" \
    --push .
else
  echo "⏩ Skipping build (--fast). Using existing image."
  docker tag "$IMAGE_NAME" "$FULL_TAG"
  docker tag "$IMAGE_NAME" "$ACR_NAME.azurecr.io/$IMAGE_NAME:latest"
fi

# === PUSH IMAGE TO ACR (fallback for --fast) ===
if [ "$SKIP_BUILD" = true ]; then
  echo "🚚 Pushing image to ACR: $FULL_TAG"
  docker push "$FULL_TAG"
  echo "🚚 Pushing image to ACR: latest"
  docker push "$ACR_NAME.azurecr.io/$IMAGE_NAME:latest"
fi

echo "🚀 Updating App Service to use the new image..."
az webapp config container set \
  --name "${APP_NAME}" \
  --resource-group "${RESOURCE_GROUP}" \
  --container-image-name "${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${TAG}" \
  --container-registry-url "https://${ACR_NAME}.azurecr.io"

# === RESTART THE APP SERVICE ===
echo "🔁 Restarting App Service..."
az webapp restart \
  --name "${APP_NAME}" \
  --resource-group "${RESOURCE_GROUP}"

# === EXTERNAL HEALTH CHECK ===
echo ""
echo "🔍 Verifying public /health endpoint..."

for i in {1..60}; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$PING_URL")
  if [[ "$STATUS" == "200" ]]; then
    echo "✅ Public FastAPI is live at $PING_URL"
    break
  else
    echo "⏳ ($i/60) Not ready yet... (HTTP $STATUS)"
    sleep 2
  fi
done

# === LOG TAIL - WHERE TO FIND ===
APP_URL="https://$APP_NAME.azurewebsites.net"
echo ""
echo "🌐 App deployed at: $APP_URL"
echo ""
echo "📡 To tail live logs:"
echo "   az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP"
echo ""

# === DEBUG CONSOLE - WHERE TO FIND ===
echo ""
echo "🧠 Debug Console:"
echo "  https://${APP_NAME}.scm.azurewebsites.net/DebugConsole"
echo "  Check LogFiles/app/eval.log or LogFiles/default_docker.log for errors"
