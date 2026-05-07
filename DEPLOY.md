# 部署指南

## 前端部署到 Vercel

### 前提条件
1. 完成 Vercel CLI 授权（浏览器点击 Allow）

### 步骤
```bash
# 1. 确认 Vercel CLI 已安装
vercel --version

# 2. 确认已登录
vercel whoami

# 3. 编译前端 H5
cd frontend && npm run build:h5

# 4. 部署到 Vercel
vercel --prod --yes dist/build/h5
```

### 当前状态
Vercel CLI 已安装（v53.1.1），等待浏览器授权完成。
授权链接：https://vercel.com/oauth/device?user_code=HLDB-FVNN

---

## 后端部署到 Render

### 前提条件
Render 不支持 Gitee 仓库，需要以下任一方式：
1. 将代码同步到 GitHub 仓库
2. 在 Render Dashboard 手动创建 Web Service 并上传 Docker 镜像

### 方式一：GitHub + Render Blueprint（推荐）
1. 在 GitHub 创建仓库 `medi-learn`
2. 推送代码到 GitHub
3. 访问 [render.com](https://render.com) → New + → Blueprint
4. 选择 GitHub 仓库，Render 会自动读取 `render.yaml`
5. 在 Dashboard 设置环境变量（从 `.env` 复制）

### 方式二：手动创建 Web Service
1. 访问 [render.com](https://render.com) → New + → Web Service
2. 选择部署方式：Deploy an existing image
3. 上传 Docker 镜像或使用 GitHub 仓库
4. 设置环境变量：
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `OPENAI_API_KEY`
   - `ALLOW_ORIGINS=["*"]`
   - 其他 `.env` 中的配置

### 已创建的文件
- `backend/Dockerfile` - Docker 镜像配置
- `backend/start.sh` - 启动脚本
- `render.yaml` - Render Blueprint 配置

---

## 环境变量清单

部署到 Render 时需要在 Dashboard 中设置以下环境变量：

```
DEBUG=false
APP_NAME=中医学习小程序
DATABASE_URL=mysql+pymysql://...
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
ALLOW_ORIGINS=["*"]
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen-turbo
```
