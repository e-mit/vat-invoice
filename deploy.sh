docker push emitz/vat-invoice:latest

gcloud config set project vat-invoice

gcloud run deploy vat-invoice-service --image emitz/vat-invoice:latest --allow-unauthenticated --region=europe-west1
