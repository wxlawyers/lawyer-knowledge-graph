"""Lawyer Knowledge Graph - Streamlit 前端"""
import streamlit as st
import httpx
import os
import json

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="律师知识图谱",
    page_icon="⚖️",
    layout="wide",
)


@st.cache_data(ttl=30)
def api_get(path: str):
    try:
        resp = httpx.get(f"{API_URL}{path}", timeout=30)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return None


def api_post(path: str, json_body: dict):
    try:
        resp = httpx.post(f"{API_URL}{path}", json=json_body, timeout=120)
        if resp.status_code == 200:
            return resp.json()
        return {"error": f"{resp.status_code}: {resp.text[:200]}"}
    except Exception as e:
        return {"error": str(e)}


# ── 侧边栏 ─────────────────────────────────────────────────

st.sidebar.title("⚖️ 律师知识图谱")
page = st.sidebar.radio("功能导航", ["案件录入", "类案检索", "知识卡片", "案件列表"])

# API 状态
health = api_get("/api/health")
if health and health.get("status") == "ok":
    st.sidebar.success("API 服务正常")
else:
    st.sidebar.error("API 服务未连接")

st.sidebar.markdown("---")
st.sidebar.caption("Lawyer Knowledge Graph v0.1.0")


# ── 案件录入 ───────────────────────────────────────────────

if page == "案件录入":
    st.header("📝 案件知识自动沉淀")
    st.caption("粘贴裁判文书或案卷摘要，AI 自动提取结构化知识卡片")

    practice_area = st.selectbox(
        "执业领域",
        ["合同纠纷", "劳动争议", "知识产权", "公司法", "房产纠纷", "其他"],
    )
    raw_text = st.text_area("案件材料", height=300, placeholder="在此粘贴裁判文书原文...")

    if st.button("🚀 提取知识卡片", type="primary", disabled=not raw_text.strip()):
        with st.spinner("AI 正在分析案件材料，约需 30 秒..."):
            result = api_post(
                "/api/cases",
                {
                    "mode": "paste",
                    "raw_text": raw_text,
                    "practice_area": practice_area,
                },
            )

        if "error" in result:
            st.error(f"提取失败：{result['error']}")
        else:
            st.success(f"✅ 案件已录入，ID: {result['case_id']}")
            extracted = result.get("extracted", {})
            st.subheader("案件信息")
            col1, col2, col3 = st.columns(3)
            col1.metric("案号", extracted.get("case_number", "—"))
            col2.metric("案由", extracted.get("case_type", "—"))
            col3.metric("法院", extracted.get("court", "—"))

            if extracted.get("result"):
                st.info(f"**裁判结果**：{extracted['result']}")

            cards = extracted.get("knowledge_cards", [])
            if cards:
                st.subheader(f"知识卡片（{len(cards)} 张）")
                card_colors = {
                    "争议焦点": "🔴",
                    "裁判规则": "🔵",
                    "法条适用": "🟢",
                    "办案经验": "🟡",
                }
                for card in cards:
                    emoji = card_colors.get(card["type"], "⚪")
                    with st.expander(f"{emoji} [{card['type']}] {card['title']}"):
                        st.write(card["content"])


# ── 类案检索 ───────────────────────────────────────────────

elif page == "类案检索":
    st.header("🔍 类案智能检索")
    st.caption("输入案件描述，基于语义相似度检索历史案件知识卡片")

    query = st.text_area(
        "案件描述",
        height=120,
        placeholder="例：买卖合同中卖方交付的货物质量不符合约定，买方拒付货款并要求赔偿损失",
    )
    col1, col2 = st.columns(2)
    top_k = col1.slider("返回结果数", 5, 30, 10)
    min_sim = col2.slider("最低相似度", 0.0, 1.0, 0.6, 0.05)

    if st.button("🔎 检索", type="primary", disabled=not query.strip()):
        with st.spinner("正在检索相似案件..."):
            result = api_post(
                "/api/search",
                {"query": query, "top_k": top_k, "min_similarity": min_sim},
            )

        if "error" in result:
            st.error(f"检索失败：{result['error']}")
        else:
            results = result.get("results", [])
            if not results:
                st.warning("未找到匹配结果，尝试降低相似度阈值")
            else:
                st.success(f"找到 {len(results)} 个匹配结果")
                for i, r in enumerate(results, 1):
                    sim = r.get("similarity", 0)
                    st.markdown(
                        f"**{i}.** 相似度 `{sim:.2%}` | "
                        f"`{r.get('card_type', '')}` | "
                        f"{r.get('case_number', 'N/A')} · {r.get('case_type', 'N/A')}"
                    )
                    st.write(f"**{r.get('title', '')}**")
                    st.caption(r.get("content", "")[:300])
                    st.divider()


# ── 知识卡片 ───────────────────────────────────────────────

elif page == "知识卡片":
    st.header("📚 知识卡片库")
    card_type = st.selectbox(
        "卡片类型",
        ["全部", "争议焦点", "裁判规则", "法条适用", "办案经验"],
    )
    data = api_get(
        f"/api/cards?page=1&size=50"
        + (f"&card_type={card_type}" if card_type != "全部" else "")
    )
    if data and "cards" in data:
        cards = data["cards"]
        if not cards:
            st.info("暂无知识卡片")
        else:
            card_colors = {
                "争议焦点": "🔴",
                "裁判规则": "🔵",
                "法条适用": "🟢",
                "办案经验": "🟡",
            }
            for card in cards:
                emoji = card_colors.get(card["card_type"], "⚪")
                with st.expander(
                    f"{emoji} [{card['card_type']}] {card['title']}"
                ):
                    st.write(card["content"])
    else:
        st.info("暂无知识卡片或 API 未连接")


# ── 案件列表 ───────────────────────────────────────────────

elif page == "案件列表":
    st.header("📁 案件列表")
    data = api_get("/api/cases?page=1&size=50")
    if data and "cases" in data:
        cases = data["cases"]
        if not cases:
            st.info("暂无案件记录")
        else:
            for case in cases:
                with st.expander(
                    f"{case.get('case_number', 'N/A')} | "
                    f"{case.get('case_type', 'N/A')} | "
                    f"{case.get('court', 'N/A')}"
                ):
                    st.write(f"**裁判结果**：{case.get('result', '—')}")
                    st.caption(f"录入时间：{case.get('created_at', '—')}")
    else:
        st.info("暂无案件记录或 API 未连接")
