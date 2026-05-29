# API接口设计

## 案件管理

### POST /api/cases
录入新案件。支持两种模式：
- **手动录入**：提交结构化JSON（案号、案由、法院等）
- **粘贴提取**：提交裁判文书/案卷摘要原文，LLM自动提取结构化信息

请求体：
```json
{
  "mode": "paste",
  "raw_text": "（2025）苏02民初123号...",
  "practice_area": "合同纠纷",
  "notes": "本案的难点在于..."
}
```

响应体：
```json
{
  "case_id": "uuid",
  "extracted": {
    "case_number": "（2025）苏02民初123号",
    "case_type": "买卖合同纠纷",
    "court": "无锡市中级人民法院",
    "claim_amount": 500000,
    "result": "部分支持原告请求...",
    "knowledge_cards": [
      {"type": "争议焦点", "title": "违约金过高是否应调减", "content": "..."},
      {"type": "裁判规则", "title": "违约金调减的裁判标准", "content": "..."},
      {"type": "法条适用", "title": "民法典第585条", "content": "..."}
    ]
  }
}
```

### GET /api/cases
分页查询案件列表。支持按案由、状态、日期范围筛选。

### GET /api/cases/{case_id}
获取案件详情 + 关联知识卡片。

## 类案检索

### POST /api/search
输入案件描述，返回相似案件 + 相关法条。

请求体：
```json
{
  "query": "买卖合同中卖方交付的货物质量不符合约定，买方拒付货款并要求赔偿损失",
  "top_k": 10,
  "min_similarity": 0.6,
  "include_law": true
}
```

响应体：
```json
{
  "results": [
    {
      "case_id": "uuid",
      "case_number": "（2025）苏02民初456号",
      "case_type": "买卖合同纠纷",
      "similarity": 0.89,
      "result": "判决被告退还货款并赔偿...",
      "knowledge_cards": [...]
    }
  ],
  "related_laws": [
    {"article": "民法典第615条", "content": "标的物质量不符合要求..."}
  ]
}
```

## 法规追踪

### GET /api/lawtrack/settings
获取当前法规追踪配置（关注的领域 + 频率）。

### PUT /api/lawtrack/settings
更新追踪配置。

### POST /api/lawtrack/run
手动触发一次法规检索。

### GET /api/lawtrack/updates
获取法规更新列表，支持分页和日期筛选。

响应体：
```json
{
  "updates": [
    {
      "id": "uuid",
      "source": "北大法宝",
      "law_name": "最高人民法院关于审理买卖合同纠纷案件适用法律问题的解释",
      "update_type": "修订",
      "summary": "本次修订主要涉及...",
      "effective_date": "2026-06-01",
      "practice_areas": ["合同纠纷"],
      "created_at": "2026-05-29T08:00:00Z"
    }
  ]
}
```

## 知识卡片管理

### GET /api/cards
分页查询知识卡片，支持按类型、关联案件、关键词筛选。

### POST /api/cards/{card_id}/regenerate
对指定知识卡片调用LLM重新生成内容。
