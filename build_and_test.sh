docker build -t emitz/vat-invoice:latest .

PORT=8000 && docker run -p 8080:${PORT} --name vat-invoice-test -e PORT=${PORT} emitz/vat-invoice:latest
# then do:
# docker rm vat-invoice-test
