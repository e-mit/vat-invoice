docker build -t emit5/vat-invoice:latest .

PORT=8000 && docker run -p 8080:${PORT} --name vat-invoice-test -e FLASK_LOG_LEVEL=DEBUG -e PORT=${PORT} --rm emit5/vat-invoice:latest
