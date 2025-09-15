# 路径更新总结

## 更新概述
将项目路径从 `/root/BAK` 更新为 `/root/campus_market`

## 已更新的文件

### 1. 启动脚本
- ✅ `start_arms.sh` - 更新工作目录路径
- ✅ `start_gunicorn_arms.sh` - 更新工作目录路径

### 2. 系统服务文件
- ✅ `campus-market-arms.service` - 更新以下路径：
  - `WorkingDirectory=/root/campus_market`
  - `ExecStart=/root/campus_market/start_gunicorn_arms.sh`

### 3. 配置文件
- ✅ `gunicorn.conf.py` - 无需更新（使用相对路径）

### 4. 文档文件
- ✅ `ARMS_DEPLOYMENT.md` - 无需更新（无硬编码路径）

## 无需更新的文件

以下文件使用相对路径或动态路径，无需更新：
- `setup_cron_transactions.sh` - 使用 `$SCRIPT_DIR` 动态获取路径
- `setup_cron.sh` - 使用 `$SCRIPT_DIR` 动态获取路径
- `setup_purchase_system.sh` - 使用 `$SCRIPT_DIR` 动态获取路径
- 所有文档文件中的路径都是 `/root/GraduationProject`（不同路径）

## 重命名后的操作步骤

1. **重命名目录**：
   ```bash
   mv /root/BAK /root/campus_market
   ```

2. **更新系统服务**（如果已安装）：
   ```bash
   sudo systemctl stop campus-market-arms
   sudo cp /root/campus_market/campus-market-arms.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl start campus-market-arms
   ```

3. **验证启动**：
   ```bash
   cd /root/campus_market
   ./start_gunicorn_arms.sh
   ```

## 注意事项

- 所有相对路径引用保持不变
- 环境变量和配置参数无需修改
- 数据库连接和Redis连接配置无需修改
- 日志文件路径使用相对路径，无需修改

## 验证清单

- [ ] 重命名目录
- [ ] 测试启动脚本
- [ ] 测试系统服务（如果使用）
- [ ] 验证应用功能正常
- [ ] 检查日志文件生成
