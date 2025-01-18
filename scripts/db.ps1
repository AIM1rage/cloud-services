param ([String]$name)

yc ydb database create $name --serverless > db.info



Add-Type -AssemblyName System.Web

$endpointString = (Get-Content -Path "db.info" | Select-Object -Index 5).split()[1]

$endpoint = $endpointString.split("\?")[0]
$database = [System.Web.HttpUtility]::ParseQueryString($endpointString.split("\?")[1])["database"]



Write-Host "Creating .env file with YDB_ENDPOINT and YDB_DATABASE parameters..."

$envFilePath = ".env"

# Write YDB_ENDPOINT and YDB_DATABASE parameters to .env file (overwrite if exists)
Set-Content -Path $envFilePath -Value "YDB_ENDPOINT=$endpoint"
Add-Content -Path $envFilePath -Value "YDB_DATABASE=$database"

Write-Host ".env file created with YDB_ENDPOINT=$endpoint and YDB_DATABASE=$database"