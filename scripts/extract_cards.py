"""
案件知识卡片自动提取脚本

从案件原文中提取结构化信息，生成知识卡片。
可独立运行：python extract_cards.py --text "裁判文书原文..." --area "合同纠纷"
"""
import argparse
import json
import os
import sys

try:
    import requests
except ImportError:
    print("请先安装 requests: pip install requests")
    sys.exit(1)


EXTRACT_PROMPT = """你是一位资深民商事律师的助手。请从以下案件材料中提取结构化信息，严格按JSON格式输出。

案件材料：
{text}

请输出以下JSON（不要输出其他内容）：
{{
  "case_number": "案号（如无法提取则为空字符串）",
  "case_type": "案由",
  "court": "审理法院",
  "claim_amount": null,
  "result": "裁判结果摘要（100字以内）",
  "knowledge_cards": [
    {{
      "type": "争议焦点",
      "title": "简短标题（15字以内）",
      "content": "详细描述（100-200字）"
    }}
  ]
}}

注意：
1. knowledge_cards的type只能是：争议焦点、裁判规则、法条适用、办案经验
2. 至少生成3个知识卡片
3. 裁判规则要提炼为可复用的裁判规则，而非单纯复述本案事实
4. 法条适用要精确到具体法条编号和内容要点
5. 办案经验是律师视角的实务技巧，如"此类案件应重点收集XX证据"
"""


def extract_cards(text: str, area: str = "") -> dict:
    """从案件原文中提取知识卡片"""
    api_key = os.getenv("LLM_API_KEY", "")
    # 支持 DeepSeek V4 Pro / Kimi K3 / GLM 5.2，均兼容 OpenAI API 格式
    base_url = os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")
    model = os.getenv("LLM_MODEL", "deepseek-chat")

    if not api_key:
        return {"error": "请设置环境变量 LLM_API_KEY"}

    prompt = EXTRACT_PROMPT.format(text=text[:8000])  # 限制输入长度

    resp = requests.post(
        f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 2000
        },
        timeout=60
    )

    if resp.status_code != 200:
        return {"error": f"LLM API调用失败: {resp.status_code} {resp.text[:200]}"}

    content = resp.json()["choices"][0]["message"]["content"]

    # 尝试解析JSON
    try:
        # 清理可能的markdown代码块标记
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
        result = json.loads(cleaned)
        return result
    except json.JSONDecodeError as e:
        return {"error": f"JSON解析失败: {e}", "raw_content": content}


def main():
    parser = argparse.ArgumentParser(description="从案件材料中提取知识卡片")
    parser.add_argument("--text", "-t", help="案件材料文本")
    parser.add_argument("--file", "-f", help="案件材料文件路径")
    parser.add_argument("--area", "-a", default="", help="执业领域")
    parser.add_argument("--output", "-o", default=None, help="输出JSON文件路径")

    args = parser.parse_args()

    text = args.text
    if not text and args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()

    if not text:
        parser.print_help()
        print("\n错误：请通过 --text 或 --file 提供案件材料")
        sys.exit(1)

    print(f"正在分析案件材料（{len(text)}字）...")
    result = extract_cards(text, args.area)

    if "error" in result and "raw_content" not in result:
        print(f"错误：{result['error']}")
        sys.exit(1)

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"结果已保存到 {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
