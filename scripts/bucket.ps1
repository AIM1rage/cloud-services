param ([String]$name)

Write-Host "Creating bucket..."

yc storage bucket create --name $name

Write-Host "Putting static objects to $name bucket"

yc storage s3api put-object `
  --body static/script.js `
  --bucket $name `
  --key script.js

yc storage s3api put-object `
  --body static/index.html `
  --bucket $name `
  --key index.html

yc storage s3api put-object `
  --body static/error.html `
  --bucket $name `
  --key error.html

Write-Host "Turning on website $name"

yc storage bucket update --name $name `
  --public-read `
  --website-settings-from-file static/settings.json
