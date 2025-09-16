# 校园跳蚤市场智能推荐平台

基于Python+Flask+MySQL的校园二手交易智能推荐系统

## 项目简介

本项目是一个基于Python技术栈构建的校园跳蚤市场智能推荐平台，集成了多种推荐算法，包括协同过滤、内容推荐和混合推荐，旨在为校园用户提供个性化的二手商品推荐服务。

## 主要功能

### 用户功能
- 用户注册、登录、个人中心管理
- 商品发布、浏览、搜索
- 个性化商品推荐
- 商品点赞、收藏、联系卖家
- 交易记录管理

### 推荐系统
- 协同过滤推荐算法
- 基于内容的推荐算法
- 混合推荐策略
- 冷启动问题处理
- 推荐效果评估

### 管理功能
- 用户管理
- 商品管理
- 分类管理
- 数据统计分析
- 推荐效果监控

## 技术栈

### 后端技术
- **Python 3.8+**: 主要开发语言
- **Flask 2.3.3**: Web框架
- **Flask-SQLAlchemy**: ORM框架
- **Flask-Login**: 用户认证
- **MySQL 8.0**: 主数据库
- **Redis**: 缓存和会话存储

### 推荐算法
- **Scikit-learn**: 机器学习库
- **Surprise**: 推荐系统库
- **Pandas**: 数据处理
- **NumPy**: 数值计算

### 前端技术
- **HTML5/CSS3/JavaScript**: 基础前端技术
- **Bootstrap 5**: UI框架
- **Font Awesome**: 图标库
- **jQuery**: JavaScript库

### 部署运维
- **Gunicorn**: WSGI服务器
- **Nginx**: Web服务器（可选）
- **Docker**: 容器化部署（可选）

## 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端展示层     │    │   应用服务层     │    │   数据存储层     │
│                │    │                │    │                │
│ • HTML/CSS/JS   │◄──►│ • Flask应用     │◄──►│ • MySQL数据库   │
│ • Bootstrap     │    │ • RESTful API   │    │ • Redis缓存     │
│ • 响应式设计     │    │ • 业务逻辑      │    │ • 文件存储      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │   推荐算法层     │
                       │                │
                       │ • 协同过滤      │
                       │ • 内容推荐      │
                       │ • 混合推荐      │
                       └─────────────────┘
```

## 安装部署

### 环境要求

- Python 3.8+
- MySQL 8.0+
- Redis 4.0+
- 操作系统: Linux/Windows/macOS

### 快速启动

1. **克隆项目**
```bash
git clone <repository-url>
cd GraduationProject
```

2. **配置数据库**
```bash
# 创建数据库
mysql -u root -p -e "CREATE DATABASE campus_market CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

3. **配置环境变量**
```bash
# 复制环境配置文件
cp .env.example .env
# 编辑配置文件，设置数据库连接信息
vim .env
```

4. **一键启动**
```bash
# 运行启动脚本
./start.sh
```

5. **访问应用**
- 主应用: http://localhost:80
- 管理后台: http://localhost:8080/admin

### 手动安装

1. **创建虚拟环境**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **初始化数据库**
```bash
python app.py init-db
```

4. **创建管理员用户**
```bash
python app.py create-admin
```

5. **启动应用**
```bash
python app.py
```

## 配置说明

### 数据库配置

在 `.env` 文件中配置数据库连接：

```env
DB_HOST=localhost
DB_PORT=5081
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=campus_market
```

### Redis配置

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

### 应用配置

```env
SECRET_KEY=your-secret-key
MAIN_PORT=80
ADMIN_PORT=8080
```

## API文档

### 商品相关API

- `GET /api/items` - 获取商品列表
- `GET /api/items/{id}` - 获取商品详情
- `POST /api/items` - 创建商品
- `PUT /api/items/{id}` - 更新商品
- `POST /api/items/{id}/like` - 点赞商品
- `POST /api/items/{id}/contact` - 联系卖家

### 推荐相关API

- `GET /api/recommendations` - 获取推荐商品
- `POST /api/recommendations/{id}/click` - 记录推荐点击

### 用户相关API

- `GET /api/users/profile` - 获取用户资料
- `PUT /api/users/profile` - 更新用户资料
- `GET /api/users/stats` - 获取用户统计

## 推荐算法说明

### 1. 协同过滤算法

基于用户行为数据，找到相似用户，推荐相似用户喜欢的商品。

**优点**: 能够发现用户潜在兴趣
**缺点**: 存在冷启动问题

### 2. 基于内容的推荐

分析商品特征和用户历史行为，推荐相似特征的商品。

**优点**: 推荐结果可解释性强
**缺点**: 推荐多样性不足

### 3. 混合推荐策略

结合协同过滤和内容推荐，通过权重融合提高推荐效果。

**优点**: 综合多种算法优势
**缺点**: 计算复杂度较高

## 数据模型

### 用户表 (users)
- id: 用户ID
- username: 用户名
- email: 邮箱
- password_hash: 密码哈希
- interests: 兴趣标签
- created_at: 创建时间

### 商品表 (items)
- id: 商品ID
- title: 商品标题
- description: 商品描述
- price: 价格
- category_id: 分类ID
- seller_id: 卖家ID
- images: 商品图片
- tags: 商品标签
- status: 商品状态

### 用户行为表 (user_behaviors)
- id: 行为ID
- user_id: 用户ID
- item_id: 商品ID
- behavior_type: 行为类型
- created_at: 行为时间

### 推荐记录表 (recommendations)
- id: 推荐ID
- user_id: 用户ID
- item_id: 商品ID
- algorithm_type: 算法类型
- score: 推荐分数
- is_clicked: 是否点击

## 性能优化

### 缓存策略
- Redis缓存推荐结果
- 缓存热门商品数据
- 缓存用户画像信息

### 数据库优化
- 添加适当的索引
- 分页查询优化
- 查询语句优化

### 前端优化
- 图片懒加载
- 静态资源压缩
- CDN加速

## 监控和日志

### 日志记录
- 应用日志: `logs/app.log`
- 错误日志: `logs/error.log`
- 访问日志: `logs/access.log`

### 性能监控
- 推荐算法性能监控
- 数据库查询性能监控
- 用户行为分析

## 开发指南

### 项目结构
```
GraduationProject/
├── app/                    # 应用主目录
│   ├── models/            # 数据模型
│   ├── views/             # 视图控制器
│   ├── services/          # 业务逻辑服务
│   ├── static/            # 静态文件
│   └── templates/         # 模板文件
├── config.py              # 配置文件
├── app.py                 # 应用入口
├── requirements.txt       # 依赖包
├── start.sh              # 启动脚本
└── README.md             # 项目说明
```

### 开发环境设置
1. 安装开发依赖
2. 配置开发数据库
3. 启用调试模式
4. 设置日志级别

### 代码规范
- 遵循PEP 8编码规范
- 使用类型注解
- 编写单元测试
- 添加文档字符串

## 常见问题

### Q: 如何重置数据库？
A: 删除数据库后重新运行 `python app.py init-db`

### Q: 如何修改推荐算法？
A: 在 `app/services/recommendation_service.py` 中修改算法逻辑

### Q: 如何添加新的商品分类？
A: 在管理后台的分类管理页面添加，或直接操作数据库

### Q: 如何优化推荐效果？
A: 调整算法权重、增加用户行为数据、优化特征工程

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目作者: [您的姓名]
- 邮箱: [您的邮箱]
- 项目地址: [项目仓库地址]

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 实现基础功能
- 集成推荐算法
- 完成管理后台

---

**注意**: 本项目仅用于学习和研究目的，请勿用于商业用途。
