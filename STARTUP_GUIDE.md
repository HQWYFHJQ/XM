# 校园跳蚤市场启动指南

## 🚀 启动脚本说明

本项目提供了多个启动脚本，确保ARMS探针能正确监控到程序运行状况：

### 1. 推荐启动脚本：`start_with_monitoring.sh`

**功能最完整的启动脚本，包含：**
- ✅ ARMS探针环境变量配置
- ✅ OpenTelemetry配置
- ✅ 进程管理（自动停止旧进程）
- ✅ ARMS探针验证
- ✅ 详细日志输出

```bash
./start_with_monitoring.sh
```

### 2. 生产环境启动脚本：`start_production.sh`

**适用于生产环境：**
- ✅ 使用 `gunicorn.conf.py` 配置文件
- ✅ 多Worker进程
- ✅ 完整的日志配置
- ✅ ARMS探针监控

```bash
./start_production.sh
```

### 3. 基础启动脚本：`start_with_arms.sh`

**基础ARMS探针配置：**
- ✅ 基本ARMS环境变量
- ✅ Gunicorn启动
- ✅ 日志文件配置

```bash
./start_with_arms.sh
```

## 📊 ARMS探针监控配置

所有启动脚本都包含以下ARMS探针配置：

```bash
# ARMS探针环境变量
export ARMS_APP_NAME=campus_market
export ARMS_LICENSE_KEY=biimgsqhcm@6ca181feeeac0da
export ARMS_REGION_ID=cn-hangzhou
export ARMS_IS_PUBLIC=True
export ARMS_ENDPOINT=https://arms-dc-hz.aliyuncs.com

# OpenTelemetry配置
export OTEL_SERVICE_NAME=campus_market
export OTEL_RESOURCE_ATTRIBUTES="service.name=campus_market,service.version=1.0.0"
export OTEL_TRACES_EXPORTER=otlp
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_ENDPOINT=https://arms-dc-hz.aliyuncs.com
export OTEL_EXPORTER_OTLP_HEADERS="Authentication=biimgsqhcm@6ca181feeeac0da"
```

## 🔧 应用架构

- **入口文件**: `wsgi.py` - WSGI入口，包含ARMS探针导入
- **配置文件**: `gunicorn.conf.py` - Gunicorn生产配置
- **应用工厂**: `app/__init__.py` - Flask应用创建
- **主应用**: `app.py` - 开发环境入口

## 📝 日志文件

启动后会在 `logs/` 目录下生成：
- `gunicorn_access.log` - 访问日志
- `gunicorn_error.log` - 错误日志

## 🌐 访问地址

应用启动后可通过以下地址访问：
- **主页**: http://localhost:80
- **管理后台**: http://localhost:80/admin
- **API接口**: http://localhost:80/api

## ⚠️ 注意事项

1. **环境要求**: 需要激活 `condavenv` conda环境
2. **端口占用**: 确保80端口未被占用
3. **ARMS探针**: 确保已安装 `aliyun-opentelemetry-instrumentation` 包
4. **数据库**: 确保MySQL服务正在运行

## 🔍 故障排除

### 1. 端口被占用
```bash
# 查看端口占用
netstat -tlnp | grep :80

# 停止占用进程
sudo kill -9 <PID>
```

### 2. ARMS探针未加载
```bash
# 验证ARMS探针
python -c "from aliyun.opentelemetry.instrumentation.auto_instrumentation import sitecustomize; print('ARMS探针正常')"
```

### 3. 应用无法启动
```bash
# 查看错误日志
tail -f logs/gunicorn_error.log

# 检查进程状态
ps aux | grep gunicorn
```

## 📞 技术支持

如有问题，请检查：
1. 日志文件中的错误信息
2. ARMS探针是否正确加载
3. 环境变量是否正确设置
4. 数据库连接是否正常
