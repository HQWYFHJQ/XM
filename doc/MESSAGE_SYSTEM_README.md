# 消息系统功能说明

## 功能概述

本次更新为校园二手电子产品交易平台添加了完整的消息系统，包括：

1. **修复按钮转圈问题** - 修复了商品详情页点赞和联系商家按钮一直转圈的问题
2. **消息系统** - 实现了完整的聊天功能，支持买家和卖家在线沟通
3. **我的消息面板** - 用户可以在"我的消息"页面统一管理所有聊天对话
4. **已读/未读功能** - 支持消息已读和未读状态管理
5. **消息保留策略** - 消息最多保存30天，自动清理过期数据
6. **悬浮聊天窗口** - 右下角聊天悬浮窗，方便快捷沟通
7. **AI交互悬浮窗** - 左下角AI助手悬浮窗，提供智能服务

## 新增文件

### 数据模型
- `app/models/message.py` - 消息系统相关数据模型
  - `Conversation` - 对话模型
  - `Message` - 消息模型
  - `MessageNotification` - 消息通知模型
  - `ChatSession` - 聊天会话模型
  - `MessageCleanupLog` - 消息清理日志模型

### 服务层
- `app/services/message_service.py` - 消息服务类，提供所有消息相关业务逻辑

### 视图层
- `app/views/message.py` - 消息相关API端点和页面视图

### 模板文件
- `app/templates/message/messages.html` - 我的消息页面
- `app/templates/message/conversation_detail.html` - 对话详情页面

### 静态资源
- `app/static/css/floating_chat.css` - 悬浮聊天窗口样式
- `app/static/css/ai_floating.css` - AI交互悬浮窗样式
- `app/static/js/floating_chat.js` - 悬浮聊天窗口JavaScript
- `app/static/js/ai_floating.js` - AI交互悬浮窗JavaScript

### 工具脚本
- `cleanup_messages.py` - 消息清理脚本
- `setup_cron.sh` - 定时任务设置脚本
- `test_messages.py` - 消息系统测试脚本

## 功能特性

### 1. 消息系统核心功能

#### 对话管理
- 支持一对一对话
- 支持商品咨询对话
- 自动创建对话（联系卖家时）
- 对话列表管理

#### 消息功能
- 发送文本消息
- 消息已读/未读状态
- 消息时间显示
- 消息搜索功能

#### 通知系统
- 新消息通知
- 未读消息计数
- 实时状态更新

### 2. 悬浮聊天窗口

#### 右下角聊天悬浮窗
- 显示对话列表
- 快速发送消息
- 实时消息更新
- 未读消息提醒
- 响应式设计

#### 左下角AI助手悬浮窗
- 商品推荐
- 价格分析
- 市场趋势
- 砍价技巧
- 商品评估
- 安全提示

### 3. 数据管理

#### 消息保留策略
- 消息保存30天
- 自动清理过期数据
- 清理日志记录

#### 定时任务
- 每天凌晨2点自动清理
- 可配置保留天数
- 详细清理日志

## API接口

### 消息相关API

#### 对话管理
- `GET /messages` - 获取我的消息页面
- `GET /messages/<conversation_id>` - 获取对话详情页面
- `GET /api/messages/conversations` - 获取对话列表API
- `POST /api/messages/start-chat` - 开始新对话API

#### 消息操作
- `POST /api/messages/send` - 发送消息API
- `GET /api/messages/<conversation_id>/messages` - 获取消息列表API
- `POST /api/messages/<conversation_id>/read` - 标记已读API
- `GET /api/messages/unread-count` - 获取未读数量API

#### 搜索功能
- `GET /api/messages/search` - 搜索消息API

#### 在线状态
- `GET /api/messages/online-users` - 获取在线用户API
- `POST /api/messages/update-session` - 更新会话状态API

## 使用方法

### 1. 联系卖家
1. 在商品详情页点击"联系卖家"按钮
2. 系统自动创建聊天对话
3. 跳转到对话详情页面开始聊天

### 2. 查看消息
1. 点击导航栏用户菜单中的"我的消息"
2. 查看所有对话列表
3. 点击对话进入聊天界面

### 3. 悬浮聊天
1. 点击右下角聊天按钮
2. 查看对话列表
3. 快速发送消息

### 4. AI助手
1. 点击左下角AI按钮
2. 选择需要的功能
3. 与AI助手对话

## 配置说明

### 数据库配置
确保MySQL数据库正常运行，端口5081，密码"4mapg]zj2Am"]9(;"

### 定时任务配置
运行以下命令设置消息清理定时任务：
```bash
./setup_cron.sh
```

### 测试功能
运行测试脚本验证消息系统：
```bash
python3 test_messages.py
```

## 技术特点

### 前端技术
- 响应式设计，支持移动端
- 实时消息更新
- 优雅的动画效果
- 无障碍支持

### 后端技术
- RESTful API设计
- 数据库事务管理
- 消息队列支持
- 定时任务管理

### 安全特性
- 用户权限验证
- 消息内容过滤
- SQL注入防护
- XSS攻击防护

## 注意事项

1. **数据库迁移**：首次运行需要创建新的数据表
2. **定时任务**：确保cron服务正常运行
3. **文件权限**：确保日志目录有写入权限
4. **内存使用**：大量消息可能影响性能，建议定期清理

## 故障排除

### 常见问题

1. **按钮仍然转圈**
   - 检查JavaScript控制台错误
   - 确认API响应格式正确

2. **消息发送失败**
   - 检查用户登录状态
   - 确认数据库连接正常

3. **悬浮窗不显示**
   - 检查CSS文件是否正确加载
   - 确认JavaScript没有错误

4. **定时任务不执行**
   - 检查cron服务状态
   - 确认脚本路径正确

### 日志查看
- 应用日志：`logs/app.log`
- 清理日志：`logs/cleanup.log`
- 错误日志：`logs/error.log`

## 更新日志

### v1.1.0 (2025-09-09)
- 修复点赞和联系商家按钮转圈问题
- 新增完整消息系统
- 新增悬浮聊天窗口
- 新增AI交互悬浮窗
- 新增消息保留策略
- 新增定时清理任务
- 优化用户体验
- 增强安全性

---

**注意**：本系统仅用于学习和研究目的，请勿用于商业用途。
