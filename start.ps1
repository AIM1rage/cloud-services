param (
  [String]$serviceAccountName,
  [String]$databaseName,
  [String]$bucketName
)

Write-Host "Creating service account..."

yc iam service-account create --name $serviceAccountName > sa.info

$serviceAccountId = (Get-Content -Path "sa.info" | Select-Object -Index 0).split()[1]



Start-Sleep -Seconds 3



Write-Host "Issuing permissions to the service account... "

yc resource-manager folder add-access-binding $Env:YC_FOLDER_ID `
  --role ydb.editor `
  --subject serviceAccount:$serviceAccountId


powershell ./scripts/db.ps1 -name $databaseName
powershell ./scripts/table.ps1 -serviceAccountId $serviceAccountId
powershell ./scripts/api.ps1 -serviceAccountId $serviceAccountId
