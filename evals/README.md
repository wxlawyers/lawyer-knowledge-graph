# Skill Evals

轻量回归测试框架，防止技能定义（description / examples）与真实使用场景脱节。

当有人改写某个技能的 frontmatter 导致其偏离原始领域（比如把 `compensation-calculator` 改成只做文书撰写），触发测试会立即失败，在 CI 中挡住合并。

## 目录结构

```
evals/
├── run_evals.py        # 运行器（含 token 化与重叠判定逻辑）
├── README.md
└── cases/              # 每个关键技能一个 JSON 用例文件
    ├── compensation-calculator.json
    ├── legal-research.json
    └── ...
```

## 用例格式

```json
{
  "skill": "compensation-calculator",
  "description": "该用例的用途说明",
  "triggers": [
    "交通事故10级伤残能赔多少",
    "工伤十级，月工资8000，能赔多少"
  ],
  "negative": [
    "帮我起草一份起诉状"
  ]
}
```

- `skill`：技能目录名，必须与 `skills/<skill>/SKILL.md` 一致
- `triggers`：应当激活该技能的自然语言表述，每条必须与技能的
  `description`/`examples` 存在至少 1 个有效 token 重叠
- `negative`：不应当激活该技能的表述，每条必须与技能定义零重叠

## 运行

```bash
# 从仓库根目录运行
python evals/run_evals.py

# 新增关键技能时，在 cases/ 下新建同名 JSON 并补充触发/负例
```

## 判定逻辑

有效 token = 中文 bigram（连续两字）+ 英文/数字单词（≥2 字符），
去掉通用连接词（帮我、一下、一份 等）。该方法不依赖外部模型，
只验证"触发语与技能定义的领域一致"，是廉价但可靠的冒烟测试。
