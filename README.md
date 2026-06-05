# hdu-campus-creative
✨ 项目简介
杭电印迹是一个面向杭州电子科技大学校园场景的AI文创盲盒生成器。它结合多模态理解、动态风格推荐、跨会话用户画像、灵感集市等能力，为用户提供极致个性化的数字艺术品生成与分享体验。无论是图书馆的午后、月雅湖的晨雾，还是实验室通宵的代码，都能变成独一无二的视觉作品。

🚀 核心特性
🎨 智能场景理解引擎 – 支持复合句、情感识别、实体链接（杭电地标/梗），甚至可上传参考图影响生成方向。

🧠 跨会话用户画像 – 持久化存储用户偏好、收藏风格、成就徽章，多设备自动合并，实现“越用越懂你”。

⚡ 渐进式图像加载 – 首屏200ms内返回文案+风格化占位图，异步生成高清图，支持指数退避重试与应急图库降级。

🖼️ 灵感集市 – 浏览他人公开发布的作品，一键“试试同款”，快速复刻创意。

📤 社交分享 – 生成短链分享作品，支持点赞、收藏、举报，热门榜单展示本周热门。

🎁 彩蛋系统 – 隐藏款画框、风格对战、时光胶囊、主题切换……惊喜不断。

🔁 用户反馈闭环 – 赞/踩实时调整推荐权重，提供“重试”机制，持续优化体验。

📦 快速开始
环境要求
Matrix 兼容平台（如 SkillHunt）

图像生成 API（通义万相 或 OpenAI 兼容接口）

Python 3.10+（本地开发测试）

安装部署
克隆仓库

bash
git clone https://github.com/yourusername/hdu-campus-creative.git
cd hdu-campus-creative
安装依赖

bash
pip install -r requirements.txt
配置环境变量

env
MATRIX_HOMESERVER=https://your.homeserver
MATRIX_ACCESS_TOKEN=your_token
IMAGE_API_KEY=your_api_key
IMAGE_API_ENDPOINT=https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis
FALLBACK_IMAGE_DIR=./assets/fallback
运行

bash
python main.py
使用方式
在 Matrix 客户端中与机器人对话：

直接输入描述文字：图书馆5楼靠窗，夕阳 → 生成一张对应风格的作品

使用命令：

/gallery – 查看个人作品画廊

/inspire – 浏览灵感集市

/hot – 查看热门作品榜

/duel @对手 – 发起风格对战

/timecapsule 2028-06-30 – 生成未来明信片

/theme 毕业季 – 切换主题

/privacy – 设置作品私密/公开

反馈：回复 赞 或 踩 优化后续推荐

🗂️ 项目结构
text
.
├── main.py                 # 入口与消息路由
├── skill.md                # 完整技术规范文档
├── references/
│   ├── commands.md         # 命令列表
│   ├── input-cleaning.md   # 口语清洗规则
│   ├── prompt-optimization.md # 风格专属关键词库
│   ├── style-guide.md      # 风格配置
│   └── easter-eggs.md      # 彩蛋触发条件
├── assets/
│   └── fallback/           # 应急图库（10张授权杭电实景图）
├── requirements.txt
└── README.md
⚙️ 配置说明
用户画像存储
优先使用 Matrix account_data，降级至 IndexedDB（Web）或 SQLite（CLI）。多设备合并以最新 last_active 为准，保留所有已收集风格并集。

风格权重学习
点赞：权重 × 1.2（上限 2.0）

踩：权重 × 0.5（下限 0.1）

已收集风格基础权重降至 0.3，鼓励探索新风格

图像生成重试策略
指数退避延迟：[2, 4, 8] 秒，最多 3 次。若全部失败，从应急图库随机选取并叠加滤镜，同时提示用户可 /retry。

🤝 贡献指南
欢迎提交 Issue 和 Pull Request。开发前请阅读：

新增风格：只需修改 references/style-guide.md

新增彩蛋：在 references/easter-eggs.md 中定义触发条件和响应

代码风格：遵循 PEP 8，使用 black 格式化

📄 许可证
MIT License © 2026 TAN90
