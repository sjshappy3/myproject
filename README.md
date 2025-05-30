# 知行旅游 - AI智能旅游助手

一个基于FastAPI和AI技术的智能旅游规划平台，集成了多种API服务，为用户提供个性化的旅游建议和行程规划。

## 🌟 项目特色

- **AI智能对话**: 集成Ollama本地大语言模型，提供智能旅游咨询
- **多源数据整合**: 整合高德地图API、MiniMax API等多种数据源
- **智能缓存系统**: 基于SQLite的高效缓存机制，提升响应速度
- **用户管理系统**: 完整的用户注册、登录、会话管理功能
- **响应式设计**: 现代化的Web界面，支持多设备访问
- **实时天气信息**: 集成天气查询功能
- **图像生成**: 支持AI生成旅游相关图片

## 🚀 功能模块

### 核心功能
- **智能旅游咨询**: 基于AI的个性化旅游建议
- **景点信息查询**: 详细的景点介绍、图片、位置信息
- **行程规划**: 智能生成旅游行程安排
- **美食推荐**: 当地特色美食介绍
- **住宿建议**: 酒店和住宿推荐
- **交通指南**: 交通方式和路线规划
- **天气查询**: 实时天气信息和预报

### 管理功能
- **用户认证**: 注册、登录、会话管理
- **缓存管理**: 缓存统计、清理、优化
- **数据管理**: 用户数据和旅游数据管理

## 🛠️ 技术栈

### 后端技术
- **FastAPI**: 现代化的Python Web框架
- **SQLite**: 轻量级数据库，用于数据存储和缓存
- **Ollama**: 本地大语言模型服务
- **Uvicorn**: ASGI服务器
- **Jinja2**: 模板引擎

### 前端技术
- **HTML5**: 现代化的网页结构
- **CSS3**: 响应式样式设计
- **JavaScript**: 交互功能实现
- **Masonry**: 瀑布流布局

### 第三方服务
- **高德地图API**: 地理信息和导航服务
- **MiniMax API**: AI图像生成和语音服务
- **Pollinations API**: 图像生成服务

## 📦 项目结构

```
final langchian project/
├── main.py                 # 主应用程序入口
├── cache_db.py            # 缓存数据库管理
├── cache_management.py    # 缓存管理路由
├── user_db.py            # 用户数据库管理
├── requirements.txt       # Python依赖包
├── .env                  # 环境变量配置
├── templates/            # HTML模板文件
│   ├── index.html        # 主页模板
│   ├── auth.html         # 认证页面
│   ├── chat.html         # 聊天页面
│   ├── travel_planner.html # 旅游规划页面
│   └── ...
├── static/               # 静态资源
│   ├── css/
│   │   └── style.css     # 样式文件
│   ├── images/           # 图片资源
│   └── js/               # JavaScript文件
├── travel_cache.db       # 旅游数据缓存数据库
└── user_data.db          # 用户数据数据库
```

## 🔧 安装和运行

### 环境要求
- Python 3.8+
- Ollama (用于本地AI模型)

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd "final langchian project"
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**

创建 `.env` 文件并配置以下变量：
```env
# 高德地图API密钥
AMAP_API_KEY=your_amap_api_key

# MiniMax API配置（可选）
MINIMAX_API_KEY=your_minimax_api_key
MINIMAX_GROUP_ID=your_minimax_group_id
```

4. **安装和启动Ollama**
```bash
# 安装Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 下载模型（推荐使用qwen2.5:7b）
ollama pull qwen2.5:7b
```

5. **运行应用**
```bash
python main.py
```

应用将在 `http://localhost:8000` 启动

## 🔑 API密钥获取

### 高德地图API
1. 访问 [高德开放平台](https://lbs.amap.com/)
2. 注册账号并创建应用
3. 获取Web服务API密钥

### MiniMax API（可选）
1. 访问 [MiniMax开放平台](https://www.minimaxi.com/)
2. 注册账号并获取API密钥

## 📱 使用说明

### 基本使用
1. **访问首页**: 打开浏览器访问 `http://localhost:8000`
2. **用户注册**: 点击用户头像进行注册或登录
3. **开始咨询**: 在聊天界面输入旅游相关问题
4. **查看推荐**: 浏览AI生成的旅游建议和行程规划

### 高级功能
- **缓存管理**: 访问 `/cache-admin` 查看和管理缓存
- **热门目的地**: 访问 `/popular-destinations` 查看热门旅游目的地
- **旅游规划**: 访问 `/travel-planner` 进行详细的行程规划

## 🔒 安全特性

- **密码加密**: 使用PBKDF2算法进行密码哈希
- **会话管理**: 基于Token的安全会话机制
- **数据验证**: 严格的输入验证和数据清理
- **环境变量**: 敏感信息通过环境变量管理

## 🚀 性能优化

- **智能缓存**: SQLite缓存系统，减少API调用
- **异步处理**: FastAPI异步特性，提高并发性能
- **数据压缩**: 优化数据传输和存储
- **CDN集成**: 静态资源优化加载

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Python Web框架
- [Ollama](https://ollama.ai/) - 本地大语言模型服务
- [高德地图](https://lbs.amap.com/) - 地理信息服务
- [MiniMax](https://www.minimaxi.com/) - AI服务平台

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件
- 创建 Pull Request

---

**知行旅游** - 让AI为您的旅行保驾护航 🌍✈️
