import os

bind = "unix:/run/nincatalog/gunicorn.sock"

# Fixed rather than CPU-derived. This host also runs nin.fan, whose config sizes
# itself as cpu_count() * 2 + 1; two such services would oversubscribe the box.
workers = int(os.environ.get("WEB_CONCURRENCY", 3))

worker_class = "gthread"
threads = 2
timeout = 30
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
accesslog = "-"
errorlog = "-"
loglevel = "info"
