$envFilePath = ".env"

Write-Host "Please enter IAM token: "

do {
    $iamToken = Read-Host
} while ([string]::IsNullOrWhiteSpace($iamToken))

# Write IAM_TOKEN parameter to .env file
Add-Content -Path $envFilePath -Value "IAM_TOKEN=$iamToken"

Write-Host ".env file updated with IAM_TOKEN=$iamToken"



Write-Host "Copying .env file to messages-table folder..."

$destFolder = "messages-table"
$archiveName = "messages-table-archive.zip"

# Copy .env file to messages-table folder
Copy-Item -Path $envFilePath -Destination "$destFolder\.env" -Force

Write-Host ".env file copied to $destFolder"

# Create archive of messages-table folder
Compress-Archive -Path $destFolder\* -DestinationPath $archiveName -Force

Write-Host "$destFolder folder archived as $archiveName"



Write-Host "Creating a function to create messages table..."

$functionName = "create-messages"

yc serverless function create --name=$functionName

yc serverless function version create `
  --function-name=$functionName `
  --runtime python312 `
  --entrypoint index.handler `
  --memory 128m `
  --execution-timeout 3s `
  --source-path $archiveName

yc serverless function allow-unauthenticated-invoke $functionName