# 法律知识Excalidraw配色规范

## 颜色定义

| 用途 | 颜色名 | Hex | 适用场景 |
|------|--------|-----|---------|
| 主节点/输入 | 蓝色 | #a5d8ff | 中心节点、法规、公司法 |
| 成功/输出 | 绿色 | #b2f2bb | 案例、实务经验、合同 |
| 警告/外部 | 橙色 | #ffd8a8 | 风险提示、格式条款 |
| 特殊/处理 | 紫色 | #d0bfff | 江苏法院、知识产权 |
| 错误/关键 | 红色 | #ffc9c9 | 刑事责任、违规后果 |
| 注释/决策 | 黄色 | #fff3bf | 情势变更、时效 |
| 数据/存储 | 青色 | #c3fae8 | 数据、财务 |

## 法律知识思维导图模板

### 中心节点
- 颜色：蓝色#a5d8ff
- 尺寸：200×80px
- 文字：标题20px

### 分支节点
- 颜色：按内容类型选择
- 尺寸：180×70px
- 文字：正文16px

### 子节点
- 尺寸：160×60px
- 文字：14-16px

## 常见法律知识图类型

### 1. 法规要点图
- 中心：法规名称（蓝色）
- 分支：各章节要点（按内容颜色区分）
- 子节点：具体条文

### 2. 案例关系图
- 中心：案由（绿色）
- 分支：争议焦点→裁判要旨→实务启示
- 颜色：问题=红色，分析=蓝色，结论=绿色

### 3. 流程图
- 起点：蓝色
- 过程：黄色
- 决策：橙色
- 结果：绿色

### 4. 对比图
- 左侧：旧规定（灰色/红色）
- 右侧：新规定（绿色/蓝色）
- 中间：变化点（黄色高亮）

## 文字规范

- 标题：fontSize 20px，fontFamily 1
- 正文：fontSize 16px，fontFamily 1
- 注释：fontSize 14px（尽量少用）
- **禁止使用fontSize低于14**
- **禁止使用emoji**（Excalidraw字体不支持）

## 容器绑定规范

```json
{
  "type": "rectangle",
  "id": "r1",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "roundness": { "type": 3 },
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "boundElements": [{ "id": "t_r1", "type": "text" }]
},
{
  "type": "text",
  "id": "t_r1",
  "x": 105,
  "y": 110,
  "width": 190,
  "height": 60,
  "text": "文字内容",
  "fontSize": 16,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "r1",
  "originalText": "文字内容",
  "autoResize": true
}
```

## 文件保存路径

- 法规思维导图：`08-裁判规则库/[分类]/[法规名]-思维导图.excalidraw`
- 案例关系图：`08-裁判规则库/[分类]/[案例名]-案例图.excalidraw`
- 流程图：`08-裁判规则库/[分类]/[主题]-流程图.excalidraw`
- 沉淀报告：`09-每日法律速报/YYYY-MM-DD-沉淀报告.excalidraw`
