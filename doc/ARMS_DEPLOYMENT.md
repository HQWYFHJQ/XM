# 阿里云ARMS云控系统部署指南

## 概述
本指南说明如何将校园跳蚤市场应用接入阿里云ARMS（Application Real-Time Monitoring Service）云控系统，实现应用监控、性能分析和故障诊断。

## 环境要求
- Python 3.9+
- Conda环境：condavenv
- 阿里云ARMS探针：aliyun-bootstrap
- Gunicorn WSGI服务器

## 配置信息
```bash
# 阿里云ARMS配置
export ARMS_APP_NAME=campus_market
export ARMS_REGION_ID=cn-hangzhou
export ARMS_LICENSE_KEY=biimgsqhcm@6ca181feeeac0da
export ARMS_IS_PUBLIC=True
```

## 部署步骤

### 1. 安装依赖
```bash
# 激活conda环境
conda activate condavenv

# 安装ARMS探针（已完成）
aliyun-bootstrap -a install

# 安装应用依赖
pip install -r requirements.txt
```

### 2. 启动方式

#### 方式1：直接启动（开发测试）
```bash
./start_arms.sh
```

#### 方式2：Gunicorn启动（推荐生产环境）
```bash
./start_gunicorn_arms.sh
```

#### 方式3：系统服务启动
```bash
# 复制服务文件
sudo cp campus-market-arms.service /etc/systemd/system/

# 重载systemd配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start campus-market-arms

# 设置开机自启
sudo systemctl enable campus-market-arms

# 查看服务状态
sudo systemctl status campus-market-arms
```

### 3. 验证部署
```bash
# 运行测试脚本
python test_arms.py

# 检查应用状态
curl http://localhost:80/

# 查看日志
tail -f logs/gunicorn_access.log
tail -f logs/gunicorn_error.log
```

## 监控功能

### 1. 应用性能监控
- 请求响应时间
- 吞吐量统计
- 错误率监控
- 数据库性能

### 2. 业务监控
- 用户注册/登录
- 商品发布/交易
- 消息发送/接收
- 推荐算法性能

### 3. 基础设施监控
- CPU使用率
- 内存使用率
- 磁盘I/O
- 网络流量

## 故障排查

### 1. 常见问题
- **探针未启动**：检查环境变量设置
- **应用无法访问**：检查端口占用和防火墙
- **监控数据缺失**：检查License Key和网络连接

### 2. 日志位置
- 应用日志：`logs/gunicorn_*.log`
- 系统日志：`journalctl -u campus-market-arms`
- ARMS探针日志：查看阿里云控制台

### 3. 性能优化
- 调整Gunicorn worker数量
- 优化数据库查询
- 启用Redis缓存
- 配置CDN加速

## 安全注意事项

1. **License Key保护**：不要将License Key提交到代码仓库
2. **网络安全**：确保ARMS_IS_PUBLIC设置正确
3. **访问控制**：限制管理接口访问
4. **数据加密**：敏感数据传输加密

## 维护操作

### 1. 重启应用
```bash
# 使用systemd
sudo systemctl restart campus-market-arms

# 手动重启
pkill -f "gunicorn.*app:app"
./start_gunicorn_arms.sh
```

### 2. 更新应用
```bash
# 停止服务
sudo systemctl stop campus-market-arms

# 更新代码
git pull origin main

# 安装新依赖
pip install -r requirements.txt

# 重启服务
sudo systemctl start campus-market-arms
```

### 3. 监控告警
- 在阿里云ARMS控制台配置告警规则
- 设置关键指标阈值
- 配置通知方式（邮件/短信/钉钉）

## 联系支持
- 阿里云ARMS文档：https://help.aliyun.com/zh/arms/
- 技术支持：通过阿里云工单系统
- 项目维护：查看项目README.md
