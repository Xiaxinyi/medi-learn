# 中医学习小程序设计方案

## Context（背景）

用户需要开发一个中医学习小程序，用于：
- 记录和查询中草药信息
- 提供试题练习功能
- 自动评分和错题本管理
- 支持跨平台部署（微信小程序、H5等）

目标用户是中医学习者，需要一个便捷的学习工具来记忆草药知识和自我测试。

## 技术选型

### 前端框架
- **uni-app** - 一套代码编译到多端（微信小程序、H5、App）
- **Vue 3 + Composition API** - 现代化响应式开发
- **TypeScript** - 类型安全

### UI组件库
- **uView UI** 或 **uni-ui** - uni-app生态的UI组件库

### 后端技术栈
- **Python + FastAPI** - 高性能异步Web框架，自动生成API文档
- 或 **Go + Gin** - 高性能、高并发，适合微服务架构
- **JWT认证** - Token-based身份验证
- **CORS配置** - 跨域请求支持

### 数据库
- **MySQL 8.0** - 关系型数据库，存储结构化数据
- **SQLAlchemy (Python)** 或 **GORM (Go)** - ORM框架
- **数据库连接池** - 提高并发性能

### 数据存储方案
- **本地缓存**：uni.setStorageSync（临时数据、离线使用）
- **云端数据库**：MySQL持久化存储（用户数据、草药库、题库）
- **文件存储**：本地文件系统或对象存储（图片资源）

### 用户认证
- **手机号验证码登录**：短信验证码验证（阿里云/腾讯云短信服务）
- **微信授权登录**：微信OAuth2.0授权
- **账号绑定**：支持手机号与微信账号绑定
- **Session管理**：JWT Token刷新机制

### 图片识别
- **百度AI开放平台** - 植物/草药识别API
- 或预留接口供后续集成

## 完整技术架构

```
┌─────────────────────────────────────────┐
│         客户端 (uni-app)                 │
│  ┌──────────┬──────────┬──────────────┐ │
│  │ 微信小程序│   H5     │    App       │ │
│  └──────────┴──────────┴──────────────┘ │
└────────────────┬────────────────────────┘
                 │ HTTPS/API
                 ↓
┌────────────────────────────────────────┐
│      Nginx (反向代理 + 负载均衡)        │
└────────────────┬───────────────────────┘
                 │
                 ↓
┌────────────────────────────────────────┐
│     应用服务器 (FastAPI / Gin)          │
│  ┌──────────────────────────────────┐  │
│  │  API路由层                        │  │
│  │  - 认证接口                       │  │
│  │  - 草药接口                       │  │
│  │  - 题库接口                       │  │
│  │  - 考试接口                       │  │
│  │  - 统计接口                       │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  业务逻辑层                       │  │
│  │  - 用户服务                       │  │
│  │  - 草药服务                       │  │
│  │  - 练习服务                       │  │
│  │  - 考试服务                       │  │
│  └──────────────────────────────────┘  │
└──────────┬─────────────────────────────┘
           │
    ┌──────┴──────┐
    ↓             ↓
┌──────────┐  ┌──────────┐
│  MySQL   │  │  Redis   │
│  数据库  │  │  缓存    │
└──────────┘  └──────────┘
```

### 部署环境要求
- **服务器**: Linux (Ubuntu/CentOS)
- **Python**: 3.9+ 或 **Go**: 1.19+
- **MySQL**: 8.0+
- **Redis**: 6.0+ (可选，用于缓存)
- **Nginx**: 最新稳定版

## 功能模块设计

### 1. 草药记录模块

#### 1.1 草药列表页
- 搜索功能（按名称、功效、性味）
- 分类浏览（解表药、清热药、补益药等）
- 收藏标记
- 最近查看记录

#### 1.2 草药详情页
**基础信息：**
- 草药名称（中文名、拉丁名、别名）
- 性味归经
- 功效主治
- 用法用量
- 注意事项/禁忌

**多媒体内容：**
- 草药图片（支持多图）
- 产地分布图

**个人笔记：**
- 添加/编辑学习笔记
- 学习心得记录
- 笔记时间线展示

**图片识别：**
- 拍照识别草药
- 从相册选择图片识别
- 识别结果确认和修正

#### 1.3 添加/编辑草药
- 手动录入草药信息
- 拍照上传
- 表单验证

### 2. 试题系统模块

#### 2.1 题库管理
**题目类型：**
- 单选题（4个选项）
- 多选题（4-6个选项，可选多个）

**题目属性：**
- 题目内容
- 选项列表
- 正确答案
- 答案解析
- 难度等级（简单/中等/困难）
- 知识点标签（关联草药）
- 题目来源

**题库分类：**
- 按章节分类
- 按难度分类
- 随机组卷

#### 2.2 练习模式
**顺序练习：**
- 按题库顺序答题
- 即时显示答案和解析

**随机练习：**
- 随机抽取题目
- 可设置题目数量

**模拟考试：**
- 设定考试时间
- 考试结束后统一评分
- 生成成绩报告

#### 2.3 智能组卷
- 选择题库范围
- 设定题目数量
- 设定难度比例
- 自动生成试卷

### 3. 评分系统模块

#### 3.1 答题评分
- 单选题：答对得满分，答错0分
- 多选题：全对得满分，部分正确按比例得分，有错误选项0分
- 实时显示得分

#### 3.2 成绩统计
- 本次考试成绩
- 历史成绩趋势图
- 各知识点正确率
- 答题用时统计

#### 3.3 排行榜（可选）
- 好友排行榜
- 全球排行榜

### 4. 错题本模块

#### 4.1 自动收集
- 答错的题目自动加入错题本
- 记录错误答案和正确答案
- 记录错误时间

#### 4.2 错题管理
- 查看错题列表
- 查看错题详情和解析
- 标记已掌握（移除错题）
- 按知识点筛选
- 按错误次数排序

#### 4.3 错题重练
- 只练习错题
- 错题强化训练
- 定期复习提醒

### 5. 个人中心模块

#### 5.1 学习统计
- 累计学习天数
- 已学习草药数量
- 已完成题目数量
- 平均正确率

#### 5.2 学习记录
- 每日学习时长
- 学习日历
- 成就系统（徽章）

#### 5.3 设置
- 通知设置
- 数据备份/恢复
- 清除缓存
- 关于我们

## 后端架构设计

### 项目结构（以Python FastAPI为例）
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # 应用入口
│   ├── config.py               # 配置文件
│   ├── database.py             # 数据库连接
│   ├── models/                 # 数据模型
│   │   ├── user.py
│   │   ├── herb.py
│   │   ├── question.py
│   │   └── exam.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py
│   │   ├── herb.py
│   │   ├── question.py
│   │   └── exam.py
│   ├── api/                    # API路由
│   │   ├── __init__.py
│   │   ├── auth.py            # 认证接口
│   │   ├── herbs.py           # 草药接口
│   │   ├── questions.py       # 题库接口
│   │   ├── exams.py           # 考试接口
│   │   └── stats.py           # 统计接口
│   ├── services/               # 业务逻辑
│   │   ├── auth_service.py
│   │   ├── herb_service.py
│   │   ├── question_service.py
│   │   └── exam_service.py
│   ├── utils/                  # 工具函数
│   │   ├── jwt_utils.py
│   │   ├── sms_utils.py
│   │   └── wechat_utils.py
│   └── middleware/             # 中间件
│       ├── auth_middleware.py
│       └── cors_middleware.py
├── tests/                      # 测试文件
├── alembic/                    # 数据库迁移
├── requirements.txt
├── .env                        # 环境变量
└── README.md
```

### 数据库表设计

#### 1. 用户表 (users)
```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    phone VARCHAR(20) UNIQUE,           -- 手机号
    wechat_openid VARCHAR(100),         -- 微信OpenID
    wechat_unionid VARCHAR(100),        -- 微信UnionID
    nickname VARCHAR(50),               -- 昵称
    real_name VARCHAR(50),              -- 真实姓名
    avatar_url VARCHAR(255),            -- 头像URL
    email VARCHAR(100),                 -- 邮箱
    gender ENUM('male', 'female', 'other') DEFAULT 'other',  -- 性别
    birthday DATE,                      -- 生日
    bio TEXT,                           -- 个人简介
    password_hash VARCHAR(255),         -- 密码哈希（可选）
    role ENUM('admin', 'user') DEFAULT 'user',  -- 角色：admin=管理者, user=使用者
    level INT DEFAULT 1,                -- 用户等级（1-10）
    experience INT DEFAULT 0,           -- 当前经验值
    total_score INT DEFAULT 0,          -- 累计得分
    streak_days INT DEFAULT 0,          -- 连续学习天数
    last_study_date DATE,               -- 最后学习日期
    status TINYINT DEFAULT 1,           -- 状态：1正常 0禁用
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_phone (phone),
    INDEX idx_email (email),
    INDEX idx_wechat_openid (wechat_openid),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 2. 草药表 (herbs)
```sql
CREATE TABLE herbs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,                     -- NULL表示系统草药，否则为个人添加
    name VARCHAR(100) NOT NULL,         -- 草药名称
    latin_name VARCHAR(200),            -- 拉丁名
    aliases JSON,                       -- 别名列表
    efficacy TEXT,                      -- 功效
    indications TEXT,                   -- 主治
    dosage VARCHAR(200),                -- 用法用量
    contraindications TEXT,             -- 禁忌
    category VARCHAR(50),               -- 分类（解表药、清热药等）
    origin VARCHAR(200),                -- 产地
    is_system TINYINT DEFAULT 0,        -- 是否系统草药
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_name (name),
    INDEX idx_category (category),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 2a. 属性标签表 (herb_attributes)
```sql
CREATE TABLE herb_attributes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,          -- 标签名称（如：温、补、升、散、燥）
    group_name VARCHAR(50),             -- 分组（如：四气、五味、升降浮沉）
    color VARCHAR(20),                  -- 显示颜色（如：#FF5722、red）
    is_system TINYINT DEFAULT 1,        -- 是否系统预设（1=系统，0=用户自定义）
    created_by BIGINT,                  -- 创建者ID（系统标签为NULL）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_name (name),          -- 标签名唯一
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_group (group_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 系统预设标签示例
-- INSERT INTO herb_attributes (name, group_name, color, is_system) VALUES
-- ('温', '四气', '#FF5722', 1),
-- ('补', '补泻', '#8BC34A', 1),
-- ('升', '升降浮沉', '#E91E63', 1),
-- ('散', '散敛', '#00BCD4', 1),
-- ('燥', '润燥', '#9C27B0', 1);
```

#### 2b. 草药-属性关联表 (herb_attribute_values)
```sql
CREATE TABLE herb_attribute_values (
    herb_id BIGINT NOT NULL,
    attribute_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (herb_id, attribute_id),  -- 联合主键防重复
    FOREIGN KEY (herb_id) REFERENCES herbs(id) ON DELETE CASCADE,
    FOREIGN KEY (attribute_id) REFERENCES herb_attributes(id) ON DELETE CASCADE,
    INDEX idx_attribute_id (attribute_id)  -- 按属性筛选索引
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

> **说明**：采用开放标签系统，不再限制为固定的五性五味。通过 `herb_attributes` 标签表 + `herb_attribute_values` 关联表实现灵活的多对多关系。标签可以分组（四气、五味、升降浮沉、补泻、润燥、散敛等），支持用户自定义扩展。

#### 关联表查询示例
```sql
-- 查询"人参"的所有属性标签
SELECT h.name,
       GROUP_CONCAT(DISTINCT CONCAT(a.group_name, ':', a.name)) as attributes
FROM herbs h
LEFT JOIN herb_attribute_values hav ON h.id = hav.herb_id
LEFT JOIN herb_attributes a ON hav.attribute_id = a.id
WHERE h.name = '人参'
GROUP BY h.id;
-- 结果：人参 | 四气:温,五味:甘,升降浮沉:升,补泻:补

-- 筛选所有带"温"标签的药
SELECT DISTINCT h.* FROM herbs h
JOIN herb_attribute_values hav ON h.id = hav.herb_id
JOIN herb_attributes a ON hav.attribute_id = a.id
WHERE a.name = '温';

-- 筛选同时带"温"和"补"标签的药
SELECT h.* FROM herbs h
JOIN herb_attribute_values hav1 ON h.id = hav1.herb_id
JOIN herb_attributes a1 ON hav1.attribute_id = a1.id AND a1.name = '温'
JOIN herb_attribute_values hav2 ON h.id = hav2.herb_id
JOIN herb_attributes a2 ON hav2.attribute_id = a2.id AND a2.name = '补';

-- 按分组筛选：查询所有"四气"分组下"寒"性的药
SELECT DISTINCT h.* FROM herbs h
JOIN herb_attribute_values hav ON h.id = hav.herb_id
JOIN herb_attributes a ON hav.attribute_id = a.id
WHERE a.group_name = '四气' AND a.name = '寒';

-- 统计各标签使用频次
SELECT a.name, a.group_name, COUNT(*) as herb_count
FROM herb_attributes a
JOIN herb_attribute_values hav ON a.id = hav.attribute_id
GROUP BY a.id
ORDER BY herb_count DESC;
```

#### 3. 草药图片表 (herb_images)
```sql
CREATE TABLE herb_images (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    herb_id BIGINT NOT NULL,
    image_url VARCHAR(500) NOT NULL,    -- 图片URL
    thumbnail_url VARCHAR(500),         -- 缩略图URL（可选）
    sort_order INT DEFAULT 0,           -- 排序
    is_cover TINYINT DEFAULT 0,         -- 是否封面图
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (herb_id) REFERENCES herbs(id) ON DELETE CASCADE,
    INDEX idx_herb_id (herb_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

> **图片上传流程**：
> 1. 前端调用 `POST /api/upload/image` 上传图片文件
> 2. 后端接收文件，保存到服务器目录（如 `/uploads/herbs/`）
> 3. 返回图片访问URL
> 4. 创建/更新草药时，将图片URL关联到 `herb_images` 表
> 5. 支持批量上传（一次最多9张）
> 6. 支持设置封面图（`is_cover = 1`）

#### 4. 草药笔记表 (herb_notes)
```sql
CREATE TABLE herb_notes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    herb_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (herb_id) REFERENCES herbs(id) ON DELETE CASCADE,
    INDEX idx_user_herb (user_id, herb_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 5. 题目表 (questions)
```sql
CREATE TABLE questions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    type ENUM('single', 'multiple') NOT NULL,  -- 题目类型
    content TEXT NOT NULL,                      -- 题目内容
    difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
    explanation TEXT,                           -- 答案解析
    tags JSON,                                  -- 知识点标签
    herb_ids JSON,                              -- 关联草药ID
    is_system TINYINT DEFAULT 1,                -- 是否系统题目
    created_by BIGINT,                          -- 创建者ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_type (type),
    INDEX idx_difficulty (difficulty)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 6. 题目选项表 (question_options)
```sql
CREATE TABLE question_options (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    question_id BIGINT NOT NULL,
    option_key VARCHAR(10) NOT NULL,            -- A, B, C, D
    content TEXT NOT NULL,
    is_correct TINYINT DEFAULT 0,               -- 是否正确选项
    sort_order INT DEFAULT 0,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    INDEX idx_question_id (question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 7. 答题记录表 (answer_records)
```sql
CREATE TABLE answer_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    question_id BIGINT NOT NULL,
    user_answers JSON,                          -- 用户选择的答案
    is_correct TINYINT,                         -- 是否正确
    score DECIMAL(5,2),                         -- 得分
    time_spent INT,                             -- 答题用时（秒）
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id),
    INDEX idx_user_id (user_id),
    INDEX idx_question_id (question_id),
    INDEX idx_answered_at (answered_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 8. 错题本表 (wrong_answers)
```sql
CREATE TABLE wrong_answers (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    question_id BIGINT NOT NULL,
    user_answers JSON,                          -- 错误答案
    correct_answers JSON,                       -- 正确答案
    wrong_count INT DEFAULT 1,                  -- 错误次数
    last_wrong_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_mastered TINYINT DEFAULT 0,              -- 是否已掌握
    mastered_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id),
    UNIQUE KEY uk_user_question (user_id, question_id),
    INDEX idx_user_mastered (user_id, is_mastered)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 9. 考试成绩表 (exam_results)
```sql
CREATE TABLE exam_results (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    exam_name VARCHAR(100),                     -- 考试名称
    total_questions INT,                        -- 总题数
    correct_count INT,                          -- 正确题数
    score DECIMAL(5,2),                         -- 总分
    max_score DECIMAL(5,2),                     -- 满分
    time_spent INT,                             -- 总用时（秒）
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_completed_at (completed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 10. 方剂表 (formulas)
```sql
CREATE TABLE formulas (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,                     -- NULL表示系统方剂，否则为个人添加
    name VARCHAR(100) NOT NULL,         -- 方剂名称
    source VARCHAR(200),                -- 来源（出自哪本书/典籍）
    category VARCHAR(50),               -- 分类（解表剂、清热剂等）
    indications TEXT,                   -- 主治/功效
    usage TEXT,                         -- 用法
    modifications TEXT,                 -- 加减变化
    precautions TEXT,                   -- 注意事项
    is_system TINYINT DEFAULT 0,        -- 是否系统方剂
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_name (name),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 11. 方剂组成表 (formula_herbs)
```sql
CREATE TABLE formula_herbs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    formula_id BIGINT NOT NULL,
    herb_id BIGINT NOT NULL,            -- 关联herbs表
    herb_name VARCHAR(100),             -- 草药名称（冗余存储，方便查询）
    dosage VARCHAR(50),                 -- 用量
    role ENUM('chief', 'deputy', 'assistant', 'envoy') DEFAULT 'assistant', 
                                        -- 君臣佐使：君药、臣药、佐药、使药
    sort_order INT DEFAULT 0,           -- 排序
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (formula_id) REFERENCES formulas(id) ON DELETE CASCADE,
    FOREIGN KEY (herb_id) REFERENCES herbs(id),
    INDEX idx_formula_id (formula_id),
    INDEX idx_herb_id (herb_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 12. 用户反馈表 (feedback)
```sql
CREATE TABLE feedback (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,            -- 反馈用户ID
    type ENUM('suggestion', 'bug', 'complaint', 'other') DEFAULT 'suggestion',  -- 反馈类型
    title VARCHAR(200) NOT NULL,        -- 标题
    content TEXT NOT NULL,              -- 内容
    contact VARCHAR(100),               -- 联系方式（可选）
    images JSON,                        -- 附件图片URL列表
    status ENUM('pending', 'processing', 'resolved', 'rejected') DEFAULT 'pending',  -- 处理状态
    admin_reply TEXT,                   -- 管理员回复
    replied_at TIMESTAMP,               -- 回复时间
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 13. 用户等级配置表 (user_levels)
```sql
CREATE TABLE user_levels (
    id INT PRIMARY KEY AUTO_INCREMENT,
    level INT NOT NULL UNIQUE,          -- 等级（1-10）
    name VARCHAR(50) NOT NULL,          -- 等级名称（如：初学者、学徒、医者...）
    icon VARCHAR(255),                  -- 等级图标URL
    min_experience INT NOT NULL,        -- 所需最小经验值
    max_experience INT NOT NULL,        -- 该等级经验值上限
    color VARCHAR(20),                  -- 等级颜色
    privileges TEXT,                    -- 等级特权说明（JSON格式）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_level (level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 等级配置示例数据
-- INSERT INTO user_levels (level, name, min_experience, max_experience, color) VALUES
-- (1, '初学者', 0, 100, '#9E9E9E'),
-- (2, '采药学徒', 100, 300, '#4CAF50'),
-- (3, '本草学子', 300, 600, '#2196F3'),
-- (4, '药堂助手', 600, 1000, '#FF9800'),
-- (5, '杏林新秀', 1000, 1500, '#9C27B0'),
-- (6, '医者仁心', 1500, 2100, '#E91E63'),
-- (7, '岐黄传人', 2100, 2800, '#F44336'),
-- (8, '国医高手', 2800, 3600, '#00BCD4'),
-- (9, '药王再世', 3600, 4500, '#FFD700'),
-- (10, '神医圣手', 4500, 999999, '#FF5722');
```

#### 14. 经验值记录表 (experience_logs)
```sql
CREATE TABLE experience_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    type VARCHAR(50) NOT NULL,          -- 经验来源类型
    description VARCHAR(200),           -- 描述
    experience INT NOT NULL,            -- 获得经验值（正数）
    balance INT NOT NULL,               -- 操作后余额
    related_id VARCHAR(100),            -- 关联业务ID（如答题记录ID）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_type (type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 15. 学习统计表 (learning_stats)
```sql
CREATE TABLE learning_stats (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    stat_date DATE NOT NULL,                    -- 统计日期
    study_duration INT DEFAULT 0,               -- 学习时长（分钟）
    herbs_viewed INT DEFAULT 0,                 -- 查看草药数
    questions_answered INT DEFAULT 0,           -- 答题数量
    correct_answers INT DEFAULT 0,              -- 正确题数
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_date (user_id, stat_date),
    INDEX idx_user_date (user_id, stat_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### API接口设计

#### 认证模块 (/api/auth)
- `POST /api/auth/send-code` - 发送短信验证码
- `POST /api/auth/login-phone` - 手机号验证码登录
- `POST /api/auth/login-wechat` - 微信授权登录
- `POST /api/auth/bind-phone` - 绑定手机号
- `POST /api/auth/refresh-token` - 刷新Token
- `GET /api/auth/profile` - 获取用户信息

#### 草药模块 (/api/herbs)
- `GET /api/herbs` - 获取草药列表（支持搜索、筛选、分页）【公开】
- `GET /api/herbs/{id}` - 获取草药详情【公开】
- `POST /api/herbs` - 添加草药【**admin**】
- `PUT /api/herbs/{id}` - 更新草药【**admin**】
- `DELETE /api/herbs/{id}` - 删除草药【**admin**】
- `POST /api/herbs/{id}/favorite` - 收藏草药【登录用户】
- `DELETE /api/herbs/{id}/favorite` - 取消收藏【登录用户】
- `GET /api/herbs/{id}/notes` - 获取草药笔记【登录用户】
- `POST /api/herbs/{id}/notes` - 添加笔记【登录用户】
- `PUT /api/herbs/notes/{note_id}` - 更新笔记【登录用户】
- `DELETE /api/herbs/notes/{note_id}` - 删除笔记【登录用户】
- `POST /api/herbs/recognize` - 图片识别草药【登录用户】

#### 题库模块 (/api/questions)
- `GET /api/questions` - 获取题目列表（支持筛选、分页）【公开】
- `GET /api/questions/{id}` - 获取题目详情【公开】
- `POST /api/questions` - 添加题目【**admin**】
- `PUT /api/questions/{id}` - 更新题目【**admin**】
- `DELETE /api/questions/{id}` - 删除题目【**admin**】
- `GET /api/questions/random` - 随机抽取题目【登录用户】

#### 练习模块 (/api/practice)
- `POST /api/practice/start` - 开始练习
- `POST /api/practice/submit-answer` - 提交答案
- `GET /api/practice/history` - 获取练习历史
- `GET /api/practice/stats` - 获取练习统计

#### 错题本模块 (/api/wrongbook)
- `GET /api/wrongbook` - 获取错题列表
- `GET /api/wrongbook/{id}` - 获取错题详情
- `POST /api/wrongbook/{id}/master` - 标记已掌握
- `POST /api/wrongbook/review` - 开始错题重练
- `DELETE /api/wrongbook/{id}` - 移除错题

#### 考试模块 (/api/exams)
- `POST /api/exams/generate` - 智能组卷
- `POST /api/exams/start` - 开始考试
- `POST /api/exams/submit` - 提交试卷
- `GET /api/exams/results` - 获取考试成绩列表
- `GET /api/exams/results/{id}` - 获取成绩详情

#### 方剂模块 (/api/formulas)
- `GET /api/formulas` - 获取方剂列表（支持搜索、筛选）【公开】
- `GET /api/formulas/{id}` - 获取方剂详情（包含组成草药）【公开】
- `POST /api/formulas` - 添加方剂【**admin**】
- `PUT /api/formulas/{id}` - 更新方剂【**admin**】
- `DELETE /api/formulas/{id}` - 删除方剂【**admin**】
- `GET /api/formulas/by-herb/{herb_id}` - 根据草药查询相关方剂【公开】

#### 统计模块 (/api/stats)
- `GET /api/stats/overview` - 获取学习概览【登录用户】
- `GET /api/stats/daily` - 获取每日学习统计【登录用户】
- `GET /api/stats/trend` - 获取学习趋势【登录用户】
- `GET /api/stats/accuracy` - 获取各知识点正确率【登录用户】

#### 图片上传模块 (/api/upload)
- `POST /api/upload/image` - 通用图片上传（返回URL）【登录用户】
  - 支持单张/多张图片
  - 限制格式：jpg/png/webp
  - 限制大小：5MB
- `POST /api/upload/avatar` - 用户头像上传【登录用户】
  - 自动裁剪为正方形
  - 生成缩略图
  - 限制大小：2MB

#### 反馈模块 (/api/feedback)
- `POST /api/feedback` - 提交反馈/建议【登录用户】
- `GET /api/feedback/my` - 获取我的反馈列表【登录用户】
- `GET /api/feedback` - 获取所有反馈列表【**admin**】
- `GET /api/feedback/{id}` - 获取反馈详情【登录用户（自己）/ **admin**】
- `PUT /api/feedback/{id}/reply` - 管理员回复反馈【**admin**】
- `PUT /api/feedback/{id}/status` - 更新反馈状态【**admin**】

#### 等级模块 (/api/levels)
- `GET /api/levels` - 获取所有等级配置【公开】
- `GET /api/levels/my` - 获取当前用户等级信息【登录用户】
- `GET /api/levels/experience-logs` - 获取经验值记录【登录用户】
- `GET /api/levels/leaderboard` - 获取等级排行榜【公开】

### 权限控制设计

#### 用户角色定义
| 角色 | 标识 | 权限范围 |
|------|------|---------|
| 管理者 | `admin` | 添加/修改/删除草药、题目、方剂；管理标签；查看所有数据 |
| 使用者 | `user` | 查看草药/题目/方剂；收藏；添加笔记；答题；查看自己的统计 |

#### 后端权限中间件
```python
# role_middleware.py 伪代码
class RoleMiddleware:
    """角色权限控制中间件"""
    
    def require_role(self, roles: List[str]):
        """装饰器：要求指定角色才能访问"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                user = request.state.user
                if user.role not in roles:
                    raise HTTPException(403, "权限不足，需要管理员权限")
                return await func(*args, **kwargs)
            return wrapper
        return decorator

# 使用示例
require_admin = RoleMiddleware().require_role(['admin'])

@app.post("/api/herbs")
@require_login
@require_admin
async def create_herb(...):
    """只有admin可以添加草药"""
    ...
```

### 用户等级与经验值规则

#### 等级配置（10级）
| 等级 | 名称 | 所需经验 | 颜色 | 特权 |
|------|------|---------|------|------|
| 1 | 初学者 | 0 | 灰色 | 基础功能 |
| 2 | 采药学徒 | 100 | 绿色 | 每日答题次数+5 |
| 3 | 本草学子 | 300 | 蓝色 | 解锁错题本分析 |
| 4 | 药堂助手 | 600 | 橙色 | 每日答题次数+10 |
| 5 | 杏林新秀 | 1000 | 紫色 | 解锁方剂学习 |
| 6 | 医者仁心 | 1500 | 粉色 | 每日答题次数+15 |
| 7 | 岐黄传人 | 2100 | 红色 | 解锁高级筛选 |
| 8 | 国医高手 | 2800 | 青色 | 每日答题次数+20 |
| 9 | 药王再世 | 3600 | 金色 | 解锁成就系统 |
| 10 | 神医圣手 | 4500 | 橙红 | 无限制 |

#### 经验值获取规则
| 行为 | 经验值 | 每日上限 | 说明 |
|------|--------|---------|------|
| 每日登录 | +10 | 1次 | 连续登录额外+5 |
| 学习草药 | +5/个 | 50 | 查看草药详情 |
| 答题正确 | +10/题 | 200 | 单选题+10，多选题+15 |
| 答题错误 | +2/题 | 40 | 鼓励学习 |
| 完成考试 | +50 | 100 | 模拟考试完成奖励 |
| 收藏草药 | +3 | 30 | 收藏行为 |
| 添加笔记 | +5 | 50 | 学习笔记 |
| 错题重练正确 | +8 | 80 | 强化学习奖励 |
| 连续学习7天 | +50 | 50 | 周连续奖励 |
| 连续学习30天 | +200 | 200 | 月连续奖励 |
| 反馈被采纳 | +30 | 无上限 | 管理员标记 |

#### 升级逻辑
```typescript
// 经验值增加时自动检查升级
function addExperience(user: User, exp: number): void {
    user.experience += exp;
    
    // 查询下一级所需经验
    const nextLevel = getLevelConfig(user.level + 1);
    if (nextLevel && user.experience >= nextLevel.minExperience) {
        user.level += 1;
        // 触发升级提示/动画
        emitLevelUp(user, user.level);
    }
}
```

#### API权限层级总结
| 权限级别 | 说明 | 示例接口 |
|---------|------|---------|
| 公开 | 无需登录 | GET /api/herbs, GET /api/questions, GET /api/formulas |
| 登录用户 | 需登录（user/admin） | 收藏、答题、笔记、查看自己的统计 |
| 管理者 | 需admin角色 | POST/PUT/DELETE 草药、题目、方剂、标签 |

#### 前端权限控制
```typescript
// 前端权限判断
const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    token: ''
  }),
  getters: {
    isAdmin: (state) => state.user?.role === 'admin',
    isLoggedIn: (state) => !!state.token
  }
});

// 页面中根据权限显示/隐藏按钮
<template>
  <!-- 只有admin显示添加按钮 -->
  <button v-if="authStore.isAdmin" @click="addHerb">添加草药</button>
  
  <!-- 普通用户只显示查看 -->
  <button @click="viewHerb">查看详情</button>
</template>
```

### 后端开发计划

#### Phase 1: 基础搭建
1. 初始化FastAPI项目
2. 配置MySQL数据库连接
3. 创建数据模型和迁移脚本
4. 实现JWT认证中间件
5. 配置CORS跨域

#### Phase 2: 认证服务
1. 短信验证码服务（集成阿里云/腾讯云）
2. 微信OAuth2.0登录
3. Token生成和验证
4. 用户信息管理

#### Phase 3: 草药API
1. CRUD接口实现
2. 搜索和筛选功能
3. 图片上传处理
4. 笔记管理接口

#### Phase 4: 题库API
1. 题目CRUD接口
2. 随机抽题算法
3. 批量导入题目

#### Phase 5: 练习和考试API
1. 答题记录保存
2. 评分逻辑实现
3. 错题本管理
4. 考试成绩统计

#### Phase 6: 统计API
1. 学习数据统计
2. 趋势分析
3. 排行榜功能

#### Phase 7: 优化和部署
1. API性能优化
2. 数据库索引优化
3. 缓存策略（Redis）
4. 本地服务器部署

### 环境要求
- Python 3.9+ 或 Go 1.19+
- MySQL 8.0+
- Redis（可选，用于缓存）
- Nginx（反向代理）

### 部署架构
```
客户端(uni-app) 
    ↓
Nginx (反向代理 + HTTPS)
    ↓
FastAPI/Gin 应用服务器
    ↓
MySQL 数据库
    ↓
Redis 缓存（可选）
```

### 草药数据 (Herb)
```typescript
interface Herb {
  id: string;
  name: string;           // 中文名称
  latinName?: string;     // 拉丁名
  aliases?: string[];     // 别名
  
  // 属性标签（开放系统）
  attributes: AttributeTag[];  // 药性标签列表（如：温、补、升、散、燥）
  
  efficacy: string;       // 功效
  indications: string;    // 主治
  dosage: string;         // 用法用量
  contraindications?: string; // 禁忌
  images: string[];       // 图片URL列表
  category: string;       // 分类
  origin?: string;        // 产地
  notes: Note[];          // 个人笔记
  isFavorite: boolean;    // 是否收藏
  createdAt: number;
  updatedAt: number;
}

// 属性标签定义
interface AttributeTag {
  id: string;
  name: string;           // 标签名（如：温、补、升、散、燥）
  groupName?: string;     // 分组（如：四气、五味、升降浮沉）
  color?: string;         // 显示颜色（如：#FF5722）
}

### 反馈数据 (Feedback)
```typescript
interface Feedback {
  id: string;
  userId: string;         // 用户ID
  type: 'suggestion' | 'bug' | 'complaint' | 'other';  // 反馈类型
  title: string;          // 标题
  content: string;        // 内容
  contact?: string;       // 联系方式
  images?: string[];      // 附件图片
  status: 'pending' | 'processing' | 'resolved' | 'rejected';  // 状态
  adminReply?: string;    // 管理员回复
  repliedAt?: number;     // 回复时间
  createdAt: number;
}
```

### 用户数据 (User)
```typescript
interface User {
  id: string;
  phone?: string;         // 手机号
  nickname?: string;      // 昵称
  realName?: string;      // 真实姓名
  avatarUrl?: string;     // 头像URL
  email?: string;         // 邮箱
  gender?: 'male' | 'female' | 'other';  // 性别
  birthday?: string;      // 生日（YYYY-MM-DD）
  bio?: string;           // 个人简介
  role: 'admin' | 'user'; // 角色
  
  // 等级系统
  level: number;          // 当前等级（1-10）
  experience: number;     // 当前经验值
  levelName: string;      // 等级名称（如：采药学徒）
  levelColor: string;     // 等级颜色
  nextLevelExp: number;   // 升级所需经验值
  levelProgress: number;  // 当前等级进度（0-100%）
  totalScore: number;     // 累计得分
  streakDays: number;     // 连续学习天数
  
  createdAt: number;
}
```

### 等级配置 (LevelConfig)
```typescript
interface LevelConfig {
  level: number;          // 等级
  name: string;           // 名称（如：初学者）
  icon?: string;          // 图标URL
  minExperience: number;  // 所需最小经验值
  maxExperience: number;  // 经验值上限
  color: string;          // 显示颜色
  privileges: string[];   // 特权说明
}
```

### 经验值记录 (ExperienceLog)
```typescript
interface ExperienceLog {
  id: string;
  userId: string;
  type: 'login' | 'study_herb' | 'answer_correct' | 'answer_wrong' | 
        'exam_complete' | 'favorite' | 'note' | 'wrongbook_review' | 
        'streak_week' | 'streak_month' | 'feedback_adopted';  // 经验来源类型
  description: string;    // 描述
  experience: number;     // 获得经验值
  balance: number;        // 操作后余额
  relatedId?: string;     // 关联业务ID
  createdAt: number;
}
```

interface Note {
  id: string;
  content: string;
  createdAt: number;
}
```

### 题目数据 (Question)
```typescript
interface Question {
  id: string;
  type: 'single' | 'multiple';  // 题目类型
  content: string;              // 题目内容
  options: Option[];            // 选项列表
  correctAnswers: string[];     // 正确答案ID列表
  explanation: string;          // 答案解析
  difficulty: 'easy' | 'medium' | 'hard'; // 难度
  tags: string[];               // 知识点标签
  herbIds?: string[];           // 关联的草药ID
  createdAt: number;
}

interface Option {
  id: string;
  content: string;
}
```

### 答题记录 (AnswerRecord)
```typescript
interface AnswerRecord {
  id: string;
  questionId: string;
  userAnswers: string[];        // 用户选择的答案
  isCorrect: boolean;           // 是否正确
  score: number;                // 得分
  timeSpent: number;            // 答题用时（秒）
  answeredAt: number;           // 答题时间
}
```

### 错题记录 (WrongAnswer)
```typescript
interface WrongAnswer {
  id: string;
  questionId: string;
  userAnswers: string[];        // 错误答案
  correctAnswers: string[];     // 正确答案
  wrongCount: number;           // 错误次数
  lastWrongAt: number;          // 最后错误时间
  isMastered: boolean;          // 是否已掌握
}
```

### 考试成绩 (ExamResult)
```typescript
interface ExamResult {
  id: string;
  examName: string;             // 考试名称
  totalQuestions: number;       // 总题数
  correctCount: number;         // 正确题数
  score: number;                // 总分
  maxScore: number;             // 满分
  timeSpent: number;            // 总用时
  completedAt: number;          // 完成时间
  records: AnswerRecord[];      // 答题详情
}
```

## 页面路由设计

```
/pages/
  ├── index/                    # 首页
  ├── herbs/
  │   ├── list.vue             # 草药列表
  │   ├── detail.vue           # 草药详情
  │   └── edit.vue             # 添加/编辑草药
  ├── quiz/
  │   ├── practice.vue         # 练习模式
  │   ├── exam.vue             # 模拟考试
  │   └── result.vue           # 成绩结果
  ├── wrongbook/
  │   ├── list.vue             # 错题列表
  │   └── review.vue           # 错题重练
  ├── stats/
  │   └── index.vue            # 学习统计
  └── profile/
      └── index.vue            # 个人中心
```

## 核心功能实现要点

### 1. 草药搜索
- 使用本地索引实现快速搜索
- 支持拼音搜索（引入pinyin库）
- 模糊匹配算法

### 2. 图片识别
- 调用百度AI API进行植物识别
- 识别结果与草药库匹配
- 用户确认和修正机制

### 3. 智能组卷算法
```typescript
// 根据条件随机抽取题目
function generateExam(config: {
  total: number;
  difficultyRatio: { easy: number; medium: number; hard: number };
  tags?: string[];
}): Question[] {
  // 1. 筛选题目池
  // 2. 按难度分层抽样
  // 3. 随机打乱
  // 4. 返回题目列表
}
```

### 4. 评分逻辑
```typescript
// 计算得分
function calculateScore(
  question: Question,
  userAnswers: string[]
): number {
  if (question.type === 'single') {
    return userAnswers[0] === question.correctAnswers[0] ? 1 : 0;
  } else {
    // 多选题评分
    const correct = new Set(question.correctAnswers);
    const user = new Set(userAnswers);
    
    // 有错误选项，0分
    if ([...user].some(a => !correct.has(a))) return 0;
    
    // 部分正确，按比例得分
    const correctCount = [...user].filter(a => correct.has(a)).length;
    return correctCount / correct.size;
  }
}
```

### 5. 数据持久化
- 使用 uni.setStorageSync 存储用户数据
- 定期备份到云端（可选）
- 导入/导出JSON格式数据

## 初始数据准备

### 示例草药数据
需要准备至少50-100种常用中草药的基础数据，包括：
- 人参、黄芪、当归、白芍等补益药
- 金银花、连翘、板蓝根等清热药
- 麻黄、桂枝、薄荷等解表药

### 示例题目数据
需要准备至少200-300道练习题，覆盖：
- 草药性味归经
- 功效主治
- 配伍禁忌
- 临床应用

## 开发计划（MVP版本 - 优先实现核心功能）

### Phase 1: 基础框架搭建
1. 初始化uni-app项目（Vue 3 + TypeScript）
2. 配置uView UI组件库
3. 创建项目目录结构和路由配置
4. 实现底部TabBar导航（首页、草药、练习、我的）
5. 配置全局状态管理（Pinia）

### Phase 2: 用户认证模块
1. 手机号验证码登录页面
2. 微信授权登录集成
3. 账号绑定功能
4. 登录状态管理
5. 短信服务接口对接

### Phase 3: 草药记录模块（核心功能1）
1. 草药列表页面
   - 搜索功能（名称、功效）
   - 分类筛选
   - 收藏标记
2. 草药详情页面
   - 基础信息展示
   - 个人笔记功能（增删改查）
   - 收藏/取消收藏
3. 添加/编辑草药
   - 表单录入（名称、性味、归经、功效等）
   - 图片上传（拍照/相册）
   - 表单验证
4. 数据持久化
   - 本地存储实现
   - 云端同步接口

### Phase 4: 试题练习模块（核心功能2）
1. 题库管理
   - 题目数据结构设计
   - 示例题目数据导入（50-100题）
2. 练习模式
   - 顺序练习（逐题作答，即时反馈）
   - 随机练习（随机抽题）
   - 答题界面（选项选择、提交答案）
   - 答案解析展示
3. 评分系统
   - 单选题评分逻辑
   - 多选题评分逻辑（部分得分）
   - 实时得分计算
4. 练习记录
   - 答题历史保存
   - 正确率统计

### Phase 5: 错题本模块（配套功能）
1. 错题自动收集
   - 答错题目自动加入
   - 错误答案记录
2. 错题列表
   - 查看错题
   - 查看答案解析
   - 标记已掌握
3. 错题重练
   - 只练错题模式
   - 随机抽取错题

### Phase 6: 个人中心和学习统计
1. 个人中心页面
   - 用户信息显示
   - 学习数据统计卡片
2. 学习统计
   - 累计学习天数
   - 已学习草药数量
   - 已完成题目数量
   - 总体正确率
3. 设置功能
   - 退出登录
   - 清除缓存
   - 关于应用

### Phase 7: 优化和测试
1. UI/UX优化
   - 加载状态优化
   - 空状态提示
   - 错误处理
2. 性能优化
   - 列表渲染优化
   - 图片懒加载
3. 多端测试
   - 微信小程序测试
   - H5端测试
4. Bug修复

### Phase 8: 高级功能（后续迭代）
1. 图片识别集成（百度AI）
2. 模拟考试功能（计时、组卷）
3. 成绩趋势图表
4. 学习日历
5. 成就系统
6. 数据导出/备份

## 关键技术点

### 1. 状态管理
使用 Pinia 或 Vuex 管理全局状态：
- 用户信息
- 学习进度
- 答题状态

### 2. 性能优化
- 列表虚拟滚动（长列表）
- 图片懒加载
- 数据分页加载
- 缓存策略

### 3. 用户体验
- 加载状态提示
- 空状态展示
- 错误处理
- 操作反馈

### 4. 兼容性
- 微信小程序兼容性测试
- H5端适配
- 不同屏幕尺寸适配

## 测试策略

### 单元测试
- 评分逻辑测试
- 组卷算法测试
- 数据转换函数测试

### 集成测试
- 答题流程测试
- 数据持久化测试
- 页面跳转测试

### 端到端测试
- 完整学习流程
- 错题本功能
- 成绩统计

## 部署方案

### 微信小程序
1. 注册微信小程序账号
2. 配置小程序AppID
3. 使用HBuilderX或CLI编译为小程序
4. 上传代码到微信平台审核

### H5部署
1. 编译为H5版本
2. 部署到静态服务器（Nginx、Vercel等）
3. 配置域名和HTTPS

## 后续扩展方向

1. **社区功能**：学习打卡、经验分享
2. **AI助手**：智能问答、学习建议
3. **课程系统**：视频课程、图文教程
4. **药材市场**：中药材信息查询
5. **方剂学习**：经典方剂配伍学习
6. **针灸穴位**：经络穴位知识库

## 风险和挑战

1. **数据准确性**：中医药知识需要专业审核
2. **版权问题**：题库内容的版权归属
3. **识别准确率**：图片识别技术的局限性
4. **用户留存**：如何提高用户活跃度

## 成功指标

- 日活跃用户数（DAU）
- 平均学习时长
- 题库完成率
- 用户满意度评分
- 错题掌握率提升
