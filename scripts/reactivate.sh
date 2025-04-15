#!/bin/bash
set -e
set -x

# reactivate.sh - Restart or recreate your Azure Web App for the Baseball Tutor
# Assumes ACR, image, and setup.sh are already available

# Configuration
RESOURCE_GROUP="baseball-tutor-rg"
APP_NAME="baseball-ai-app"
SETUP_SCRIPT="./setup.sh"

echo "🔍 Checking if app $APP_NAME exists..."

if az webapp show --name "$APP_NAME" --resource-group "$RESOURCE_GROUP" &> /dev/null; then
  echo "✅ App exists. Restarting..."
  az webapp start --name "$APP_NAME" --resource-group "$RESOURCE_GROUP"
else
  echo "⚠️ App not found. Running setup script to recreate it..."
  if [ -f "$SETUP_SCRIPT" ]; then
    bash "$SETUP_SCRIPT"
  else
    echo "❌ Setup script not found at $SETUP_SCRIPT. Please check the path."
    exit 1
  fi
fi

APP_URL="https://$APP_NAME.azurewebsites.net"
echo "🌐 Your app should be available at: $APP_URL"
