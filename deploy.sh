docker push emit5/vat-invoice:latest

gcloud config set project vat-invoice

gcloud run deploy vat-invoice-service --image emit5/vat-invoice:latest --allow-unauthenticated --region=europe-west1
