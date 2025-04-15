# ⚙️ Azure Deployment Notes for Baseball Tutor App

## 🔐 Managed Identity for ACR Pulls

To enable the Azure Web App to pull from Azure Container Registry:

1. Assign system-assigned identity:
   ```bash
   az webapp identity assign --name $APP_NAME --resource-group $RESOURCE_GROUP
   ```

2. Grant it `AcrPull` on the ACR:
   ```bash
   PRINCIPAL_ID=$(az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP --query identity.principalId --output tsv)
   ACR_ID=$(az acr show --name $ACR_NAME --query id --output tsv)
   az role assignment create --assignee $PRINCIPAL_ID --role acrpull --scope $ACR_ID
   ```

3. Enable identity-based ACR pull:
   ```bash
   az resource update \
     --ids $(az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP --query id --output tsv)/config/web \
     --set properties.acrUseManagedIdentityCreds=true
   ```

> 🔥 Clean up any `DOCKER_*` app settings that override identity-based pull:
```bash
az webapp config appsettings delete \
  --name $APP_NAME --resource-group $RESOURCE_GROUP \
  --setting-names DOCKER_REGISTRY_SERVER_URL DOCKER_CUSTOM_IMAGE_NAME
```

---

## 🏷️ Docker Tagging: `latest` Is Required

Azure pulls the `:latest` tag by default unless configured otherwise.

Update `docker buildx build` in your deploy script to include:

```bash
--tag $FULL_TAG \
--tag $ACR_NAME.azurecr.io/$IMAGE_NAME:latest \
--push .
```

Or explicitly push both if using separate `docker push` step:
```bash
docker push "$FULL_TAG"
docker push "$ACR_NAME.azurecr.io/$IMAGE_NAME:latest"
```

---

## 🚦 App Startup Diagnostics

### ✅ Stream Logs to deploy.log

At the top of `start.sh`:

```bash
exec > >(tee -a /app/deploy.log) 2>&1
```

This captures all logs to `deploy.log` for easier debugging.

### ✅ Add Clear Startup Status Logs

In `start.sh`, add logs after key events:

```bash
echo "📦 Loading knowledge graph..."
# your load line
echo "✅ Knowledge graph loaded."

echo "⚙️ Starting FastAPI..."
# uvicorn ...
```

### ✅ Confirm Health Route Exists

FastAPI should expose:

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

So `curl http://localhost:8001/health` works in warm-up check.

---

## 🛡️ Optional Cleanup

- Check your current image tags:
  ```bash
  az acr repository show-tags --name $ACR_NAME --repository $IMAGE_NAME --output table
  ```

- Restart app manually post-deploy:
  ```bash
  az webapp restart --name $APP_NAME --resource-group $RESOURCE_GROUP
  ```

---

✅ You're now deploy-ready and panic-free. Go get that win, Coach!
