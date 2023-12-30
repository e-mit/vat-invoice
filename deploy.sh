docker tag release:latest emit5/vat-invoice:{sha}

docker push emit5/vat-invoice:{sha}

gcloud auth activate-service-account vat-invoice-uploader@vat-invoice.iam.gserviceaccount.com --key-file=/path/key.json --project=vat-invoice

gcloud run deploy vat-invoice-service --image emit5/vat-invoice:{sha} --allow-unauthenticated --region=europe-west1 --cpu-boost --session-affinity
