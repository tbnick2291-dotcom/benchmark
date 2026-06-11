# LLM Benchmark 平台设计文档

## 项目概述

构建一个面向团队/实验室使用的LLM综合评测平台，支持局域网部署，采用对抗式评测方式（模型互评），动态生成评测题目，覆盖知识、推理、代码、安全等多维度评测能力。

---

## 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        团队局域网                                │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│  │ 用户浏览器 │    │  CLI工具  │    │ 外部脚本  │    │  其他系统  │   │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘   │
│       │              │              │              │            │
│       └──────────────┴──────────────┴──────────────┘            │
│                          │                                       │
│                    ┌─────▼─────┐                                 │
│                    │  FastAPI  │                                 │
│                    │  服务端口  │                                 │
│                    └─────┬─────┘                                 │
│                          │                                       │
│  ┌───────────────────────┼───────────────────────┐              │
│  │                       │                       │              │
│  │  ┌─────────┐   ┌─────▼─────┐   ┌─────────┐   │              │
│  │  │对抗引擎 │◄──│评测核心  │──►│报告生成 │   │              │
│  │  └─────────┘   └─────────┘   └─────────┘   │              │
│  │       │             │             │         │              │
│  │       │       ┌─────▼─────┐       │         │              │
│  │       │       │题目生成器 │       │         │              │
│  │       │       └─────────┘       │         │              │
│  │       │             │             │         │              │
│  │       └─────────────┴─────────────┘         │              │
│  │                                             │              │
│  │            Benchmark Core 模块              │              │
│  └─────────────────────────────────────────────┘              │
│                          │                                       │
│              ┌───────────┴───────────┐                          │
│              │                       │                          │
│        ┌─────▼─────┐           ┌─────▼─────┐                   │
│        │   vLLM    │           │ PostgreSQL │                   │
│        │  推理服务  │           │   数据库   │                   │
│        └──────────┘           └──────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

### 核心模块职责

| 模块 | 职责 |
|------|------|
| **评测核心** | 协调评测流程、调度模型对战、计算积分排名 |
| **对抗引擎** | 执行模型互评对战，记录胜负结果，管理攻击策略 |
| **题目生成器** | 动态生成评测题目（模板生成 + 对抗生成） |
| **报告生成** | 多维度报告、弱点诊断、排行榜输出 |
| **vLLM推理层** | 加载本地模型、提供推理接口、管理推理队列 |
| **API层** | HTTP接口供Web/CLI/外部系统调用 |

---

## 数据模型

### PostgreSQL 数据表设计

```sql
-- 1. 模型注册表
CREATE TABLE models (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL UNIQUE,
    model_path      VARCHAR(500) NOT NULL,
    config          JSONB,
    status          VARCHAR(20) DEFAULT 'inactive',
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

-- 2. 评测任务表
CREATE TABLE evaluation_tasks (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    dimension       VARCHAR(50) NOT NULL,
    task_type       VARCHAR(50) NOT NULL,
    config          JSONB,
    status          VARCHAR(20) DEFAULT 'pending',
    created_by      INTEGER REFERENCES models(id),
    created_at      TIMESTAMP DEFAULT NOW(),
    completed_at    TIMESTAMP
);

-- 3. 评测题目表
CREATE TABLE questions (
    id              SERIAL PRIMARY KEY,
    task_id         INTEGER REFERENCES evaluation_tasks(id),
    content         TEXT NOT NULL,
    category        VARCHAR(100),
    difficulty      VARCHAR(20),
    generation_type VARCHAR(50) NOT NULL,
    attacker_id     INTEGER REFERENCES models(id),
    expected_answer TEXT,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- 4. 对战记录表
CREATE TABLE battles (
    id              SERIAL PRIMARY KEY,
    question_id     INTEGER REFERENCES questions(id),
    attacker_id     INTEGER REFERENCES models(id),
    defender_id     INTEGER REFERENCES models(id),
    attacker_answer TEXT,
    defender_answer TEXT,
    winner          VARCHAR(20),
    judge_reason    TEXT,
    judged_by       INTEGER REFERENCES models(id),
    battle_time     TIMESTAMP DEFAULT NOW()
);

-- 5. Elo积分表
CREATE TABLE elo_ratings (
    id              SERIAL PRIMARY KEY,
    model_id        INTEGER REFERENCES models(id),
    dimension       VARCHAR(50),
    rating          FLOAT DEFAULT 1500,
    wins            INTEGER DEFAULT 0,
    losses          INTEGER DEFAULT 0,
    ties            INTEGER DEFAULT 0,
    updated_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(model_id, dimension)
);

-- 6. 模型弱点分析表
CREATE TABLE weakness_analysis (
    id              SERIAL PRIMARY KEY,
    model_id        INTEGER REFERENCES models(id),
    category        VARCHAR(100),
    fail_rate       FLOAT,
    typical_errors  JSONB,
    attack_patterns JSONB,
    last_updated    TIMESTAMP DEFAULT NOW()
);

-- 7. 评测报告表
CREATE TABLE reports (
    id              SERIAL PRIMARY KEY,
    model_id        INTEGER REFERENCES models(id),
    task_ids        INTEGER[],
    report_type     VARCHAR(50),
    content         JSONB,
    generated_at    TIMESTAMP DEFAULT NOW()
);
```

---

## 评测流程

### 对抗评测流程

**Phase 1: 初始化**
- 用户选择评测维度 → 选择参赛模型 → 配置对战轮数

**Phase 2: 模型轮流扮演攻击者/防守者**

```
Round N 对战:
  模型A (攻击者) → 生成攻击题目（知识盲区/逻辑陷阱/安全边界）
  模型B (防守者) → 回答题目
  评判环节 → 攻击者自评 或 第三方裁判
  记录胜负 → 更新Elo积分
  角色互换 → 模型B攻击模型A
```

**Phase 3: 迭代多轮对战**
- 模型学习对手弱点，下轮攻击更精准
- 记录历史战绩，计算胜率趋势
- 发现稳定弱点，写入weakness_analysis

**Phase 4: 生成报告**
- Elo排行榜（整体 + 分维度）
- 各模型弱点诊断报告
- 攻击/防守成功率分析

### 攻击题目生成策略

| 评测维度 | 攻击策略 |
|---------|---------|
| 知识型 | 知识盲区、边界知识、易混淆概念 |
| 推理型 | 多步推理陷阱、逻辑循环、反直觉数学题 |
| 代码型 | 边界条件、隐藏bug场景、复杂依赖关系 |
| 安全型 | 伦理边界试探、有害请求变体、社会工程攻击 |

### Elo积分计算

采用标准Elo公式：
```
R_new = R_old + K × (S - E)

K = 32（可配置）
S = 实际结果（胜=1, 负=0, 平=0.5）
E = 预期胜率 = 1 / (1 + 10^(R_opponent - R_self)/400)
```

---

## API接口设计

### 接口概览

| 模块 | 路径 | 主要接口 |
|------|------|---------|
| 模型管理 | `/api/v1/models` | GET/POST列表，POST load/unload |
| 评测任务 | `/api/v1/tasks` | GET/POST任务，POST start/pause |
| 对战管理 | `/api/v1/battles` | GET列表/详情，POST manual |
| 排行榜 | `/api/v1/leaderboard` | GET整体/分维度排行榜 |
| 报告 | `/api/v1/reports` | GET列表/详情，POST generate |
| 系统 | `/api/v1/system` | GET status/gpu/queue/health |

---

## 前端功能模块

### 页面结构

| 页面 | 路径 | 核心功能 |
|------|------|---------|
| 仪表盘 | `/dashboard` | 模型状态、运行任务、排行榜快照、GPU状态 |
| 模型管理 | `/models` | 模型列表、注册、配置、加载/卸载 |
| 评测任务 | `/tasks` | 任务列表、创建、进度监控、题目预览 |
| 排行榜 | `/leaderboard` | 分维度排名、积分趋势图、对比分析 |
| 对战详情 | `/battles/{id}` | 题目展示、双方回答对比、评判结果 |
| 报告中心 | `/reports` | 报告列表、生成、详情、导出 |
| 系统监控 | `/system` | GPU监控、任务队列、日志查看 |

---

## 技术栈

| 层级 | 技术选型 |
|------|---------|
| 后端框架 | FastAPI |
| 推理引擎 | vLLM |
| 数据库 | PostgreSQL + SQLAlchemy |
| 前端框架 | Vue 3 + Vite |
| UI组件库 | Element Plus |
| 图表可视化 | ECharts |
| 任务调度 | APScheduler |
| 配置管理 | Pydantic + YAML |

---

## 项目结构

```
llm-benchmark/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── main.py          # FastAPI入口
│   │   ├── config.py        # 配置加载
│   │   ├── api/v1/          # API路由
│   │   ├── core/            # 核心模块（评测/对抗/题目生成/Elo/报告）
│   │   ├── inference/       # vLLM推理层
│   │   ├── db/              # 数据库层
│   │   ├── schemas/         # Pydantic模型
│   │   ├── tasks/           # 后台任务
│   │   └── utils/           # 工具函数
│   ├── alembic/             # 数据库迁移
│   ├── tests/               # 测试
│   └── requirements.txt
│
├── frontend/                # 前端应用
│   ├── src/
│   │   ├── api/             # API调用封装
│   │   ├── components/      # 公共组件
│   │   ├── views/           # 页面视图
│   │   ├── router/          # 路由配置
│   │   ├── stores/          # Pinia状态管理
│   │   └── utils/           # 工具函数
│   └── package.json
│
├── cli/                     # CLI工具
│   ├── benchmark_cli/
│   │   └── commands/        # model/task/report/status命令
│   └── setup.py
│
├── docs/                    # 文档
├── scripts/                 # 部署脚本
├── config/                  # 配置文件
├── docker/                  # Docker部署
├── README.md
└── Makefile
```

---

## 部署说明

### 局域网部署要求

- 服务器需有GPU资源（推荐24GB+显存）
- PostgreSQL数据库服务
- 局域网内可访问的IP地址
- 前端静态资源部署在同一服务器或独立服务器

### 启动流程

1. 配置 `config/config.yaml`（数据库连接、GPU设置）
2. 初始化数据库：`scripts/init_db.sh`
3. 启动后端：`scripts/start.sh`（启动FastAPI + vLLM服务）
4. 启动前端：访问 `http://<server-ip>:8080`
5. 团队成员通过局域网IP访问Web界面

---

## 初版功能范围

**初版核心功能：**
- 模型注册与管理（本地vLLM模型）
- 对抗式评测任务创建与执行
- Elo积分排行榜（整体 + 分维度）
- 基础报告生成（排行榜 + 弱点摘要）
- Web界面基础功能
- CLI工具基础命令

**后续迭代功能：**
- API接口开放（外部系统集成）
- 更丰富的报告类型和可视化
- 历史数据分析和趋势追踪
- 多GPU并行评测
- 评测任务调度优化