# Caveman-Mode-lossless-claw

整合三个省 Token 能力的 OpenClaw 配置包。40M 日额度可用对话量提升 **2.6 倍**。

## 三个省 Token 能力

- **Caveman 输出风格** — 输出 -70%（精简、去 filler、去重复）
- **lossless-claw** — 历史 -89%（压缩为摘要）
- **FAISS 本地记忆** — 背景 -120 tokens/轮（避免重复投喂）

综合节省: **61-70%**

## 文件

- `SOUL.md` — 输出风格 + Auto Tools 规则
- `tools/token_tracker.py` — tiktoken 自动计数
- `tools/local_memory.py` — FAISS 本地记忆（无需 API）
- `openclaw-config.json` — lossless-claw 参数

## 安装

1. 复制到 `~/.qclaw/workspace/`
2. 重启 OpenClaw Gateway

## 使用

每次对话: 搜记忆 → 工作 → 记token → 存要点
