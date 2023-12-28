# Gunicorn settings for Google cloud Run: one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
loglevel = "info"
errorlog = "-"  # stderr
accesslog = "-"  # stdout
worker_tmp_dir = "/dev/shm"
timeout = 0
workers = 1
threads = 8
