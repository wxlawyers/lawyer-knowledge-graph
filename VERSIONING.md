# 技能版本规范

> 本仓库的技能使用语义化版本号（`主版本.次版本.补丁`），写在每个 `SKILL.md` 的 `version` 字段里。
> 变更记录见 [CHANGELOG.md](CHANGELOG.md)。

## 一、什么时候升哪一位

| 位 | 什么时候升 | 例子 |
|----|------------|------|
| **主版本** `X+1.0.0` | 技能的**身份或边界**变了：重命名、拆分、与其他技能合并、删除；或适用范围/触发边界发生实质变化 | 某技能被并入另一技能；某技能适用领域从"民商事"收窄为"建设工程" |
| **次版本** `X.Y+1.0` | **内容**变了：新增步骤/模块/参考文件/脚本，修订流程、标准、口径 | 新增 LPR 计算模块；检索口径从 A 工具改为 B 工具；新增三层校验流程 |
| **补丁** `X.Y.Z+1` | **不影响用法**的修正：错别字、格式、失效链接、表述微调 | 修正一处断链；统一标点 |

判断不了的时候按"就高不就低"处理：拿不准是补丁还是次版本，就升次版本。

## 二、什么算"一次改动"

**任何一次合并进 master 的技能内容变更，都算一次改动**，包括：

- `SKILL.md` 正文与 frontmatter（`description`、`examples` 等）的修改；
- `references/`、`templates/`、`assets/`、`scripts/` 下的增删改；
- 技能目录的重命名、拆分、合并、删除。

**不算改动**的情况：仓库级文件（README、CHANGELOG、CI 脚本等）的修改，不影响技能版本号。

## 三、怎么操作

### 手动

改完内容后，顺手把 `SKILL.md` 里的 `version` 升一位，并在**同一次提交**里更新 `CHANGELOG.md`。

### 用脚本升版本

```bash
python3 scripts/bump_version.py legal-research --level minor
python3 scripts/bump_version.py contract-review evidence-organization --level minor
python3 scripts/bump_version.py some-skill --level patch
python3 scripts/bump_version.py old-skill --level major --dry-run   # 只看结果，不写入
```

### 提交前自检

```bash
python3 scripts/check_versions.py             # 与上一个提交比较
python3 scripts/check_versions.py --base HEAD~2
```

脚本会列出「内容改了但版本号没动」的技能。CI 会跑同样的检查。

## 四、CI 会拦住什么

`.github/workflows/skill-check.yml` 的 `version-check` 任务在 push 与 PR 时比较当前提交与上一个提交：

- 技能目录内容有变更、但该技能的 `version` 没有提升 → **失败**；
- 版本号不是 `X.Y.Z` 格式 → 由 `validate_skills.py` 拦下。

只改仓库级文件（README、CI、CHANGELOG）不会触发，因为检查只看 `skills/` 目录下的改动。

确有需要跳过时（例如批量回滚），在提交信息里写 `[skip version-check]`。

## 五、变更记录怎么写

`CHANGELOG.md` 按日期倒序，每条包含：

1. 日期与提交号；
2. 涉及哪些技能、版本从多少到多少；
3. **改了什么**——一句话说清楚，便于日后判断要不要重新读这个技能。

不要只写"更新技能"，要写清楚改了哪一部分、为什么改。
