#!/bin/bash
set -e
set -x

# status.sh - Show current app status, container image, and logs

RESOURCE_GROUP="baseball-tutor-rg"
APP_NAME="baseball-ai-app"

echo "📡 Checking status for: $APP_NAME"

echo "🔍 App state:"
az webapp show --name "$APP_NAME" --resource-group "$RESOURCE_GROUP" \
  --query "{State: state, DefaultHostName: defaultHostName}" --output table

echo ""
echo "📦 Current container image:"
az webapp config container show --name "$APP_NAME" --resource-group "$RESOURCE_GROUP" \
  --query "docker.customImageName" --output tsv

echo ""
echo "🔧 App settings (env vars):"
az webapp config appsettings list --name "$APP_NAME" --resource-group "$RESOURCE_GROUP" --output table

echo ""
echo "📄 Recent logs (use Ctrl+C to stop):"
az webapp log tail --name "$APP_NAME" --resource-group "$RESOURCE_GROUP"
