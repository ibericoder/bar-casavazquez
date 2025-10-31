# Deploy Casa Vazquez to PRODUCTION Cloud Run instance
# WARNING: This updates the LIVE site!

$PROJECT_ID = "casavazquez-470814"
$REGION = "europe-central2"
$SERVICE_NAME = "casavazquez-website-update"
$IMAGE_NAME = "gcr.io/$PROJECT_ID/$SERVICE_NAME"

Write-Host "=====================================" -ForegroundColor Red
Write-Host "⚠️  PRODUCTION DEPLOYMENT ⚠️" -ForegroundColor Red
Write-Host "=====================================" -ForegroundColor Red
Write-Host "Service: $SERVICE_NAME" -ForegroundColor Yellow
Write-Host "Region: $REGION" -ForegroundColor Yellow
Write-Host ""

$confirmation = Read-Host "Are you sure you want to deploy to PRODUCTION? (yes/no)"
if ($confirmation -ne "yes") {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Pushing local commits..." -ForegroundColor Green
git push

# Set the project
gcloud config set project $PROJECT_ID

# Build the Docker image
Write-Host ""
Write-Host "Building Docker image..." -ForegroundColor Green
gcloud builds submit --tag $IMAGE_NAME

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}

# Deploy to Cloud Run PRODUCTION instance
Write-Host ""
Write-Host "Deploying to Cloud Run PRODUCTION service..." -ForegroundColor Green
gcloud run deploy $SERVICE_NAME `
    --image $IMAGE_NAME `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --memory 512Mi `
    --cpu 1 `
    --max-instances 10 `
    --port 8080

if ($LASTEXITCODE -ne 0) {
    Write-Host "Deployment failed!" -ForegroundColor Red
    exit 1
}

# Get the service URL
Write-Host ""
Write-Host "Getting service URL..." -ForegroundColor Green
$SERVICE_URL = gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format "value(status.url)"

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "✅ PRODUCTION deployment successful!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Production URL: $SERVICE_URL" -ForegroundColor Yellow
Write-Host "Admin Panel: $SERVICE_URL/admin" -ForegroundColor Yellow
Write-Host ""
