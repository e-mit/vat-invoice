export FLASK_SECRET_KEY=$(openssl rand -base64 32)
export CSRF_SECRET=$(openssl rand -base64 32)

# Gunicorn settings for Google cloud Run: one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
