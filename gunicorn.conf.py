# Gunicorn配置文件
# 用于生产环境部署

import multiprocessing
import os

# 服务器套接字
bind = "0.0.0.0:80"
backlog = 2048

# Worker进程
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2

# 重启
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# 日志
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 进程命名
proc_name = "campus_market"

# 安全
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# 确保日志目录存在
os.makedirs("logs", exist_ok=True)
