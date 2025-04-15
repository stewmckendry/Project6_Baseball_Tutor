#!/bin/bash
set -e
set -x

# deactivate.sh - Stop or delete your Azure Web App for the Baseball Tutor

RESOURCE_GROUP="baseball-tutor-rg"
APP_NAME="baseball-ai-app"

echo "⚙️ Deactivate Options for $APP_NAME"
echo "1. Stop the app (can restart later)"
echo "2. Delete the app completely"
read -p "Choose an option [1/2]: " OPTION

if [ "$OPTION" == "1" ]; then
  echo "🛑 Stopping app $APP_NAME..."
  az webapp stop --name "$APP_NAME" --resource-group "$RESOURCE_GROUP"
  echo "✅ App stopped. You can reactivate it with reactivate.sh"
elif [ "$OPTION" == "2" ]; then
  read -p "❗ This will permanently delete the app. Are you sure? (y/n): " CONFIRM
  if [[ "$CONFIRM" == "y" || "$CONFIRM" == "Y" ]]; then
    echo "🔥 Deleting app $APP_NAME..."
    az webapp delete --name "$APP_NAME" --resource-group "$RESOURCE_GROUP"
    echo "✅ App deleted. Use reactivate.sh to recreate it later."
  else
    echo "❎ Deletion cancelled."
  fi
else
  echo "❌ Invalid option. Please choose 1 or 2."
fi
