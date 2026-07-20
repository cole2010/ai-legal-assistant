import streamlit as st
import requests
import json
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Legal AI Assistant",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Legal AI Assistant")
st.caption("Paste a legal clause — get a plain‑English breakdown, risk analysis, or summary.")

# ---------- API URL (CHANGE THIS TO YOUR LIVE RAILWAY URL) ----------
API_URL = "https://ai-legal-assistant-production-419a.up.railway.app"

# ---------- SESSION STATE ----------
if "response" not in st.session_state:
    st.session_state.response = ""
if "text" not in st.session_state:
    st.session_state.text = ""

# ---------- SAMPLE CLAUSES ----------
sample_clauses = {
    "📄 NDA Sample": "This agreement is effective as of the date signed by both parties. Confidential information includes all business, financial, and technical data.",
    "📄 Termination Sample": "Either party may terminate this agreement with thirty (30) days written notice. Upon termination, all confidential information must be returned or destroyed.",
    "📄 Liability Sample": "Neither party shall be liable for any indirect, incidental, or consequential damages arising out of this agreement.",
}

# ---------- LAYOUT ----------
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("### 📝 Enter Legal Text")
    text = st.text_area("", height=200, key="text_input", value=st.session_state.text)

with col2:
    st.markdown("### ⚡ Actions")
    analyze = st.button("🔍 Analyze Risks", use_container_width=True)
    summarize = st.button("📄 Summarize", use_container_width=True)
    clear = st.button("🧹 Clear", use_container_width=True)

with col3:
    st.markdown("### 📂 Samples")
    for label, sample in sample_clauses.items():
        if st.button(label, use_container_width=True):
            st.session_state.text = sample
            st.rerun()

# ---------- CLEAR ----------
if clear:
    st.session_state.text = ""
    st.session_state.response = ""
    st.rerun()

# ---------- API CALL ----------
def call_api(endpoint, payload):
    try:
        res = requests.post(f"{API_URL}/{endpoint}", json=payload, timeout=120)
        if res.status_code == 200:
            data = res.json()
            return data.get("analysis") or data.get("summary") or data.get("response") or "⚠️ No content in response."
        else:
            return f"⚠️ API error: {res.status_code} - {res.text}"
    except Exception as e:
        return f"⚠️ Could not reach API: {e}"

# ---------- ANALYZE ----------
if analyze and text:
    with st.spinner("Analyzing..."):
        result = call_api("analyze", {"text": text})
        st.session_state.response = result
        st.success("✅ Analysis complete")
        st.markdown("### 📊 Analysis")
        st.write(result)

# ---------- SUMMARIZE ----------
if summarize and text:
    with st.spinner("Summarizing..."):
        result = call_api("summarize", {"text": text})
        st.session_state.response = result
        st.success("✅ Summary complete")
        st.markdown("### 📄 Summary")
        st.write(result)

# ---------- RESPONSE ACTIONS ----------
if st.session_state.response:
    st.divider()
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.download_button(
            label="📥 Download as .txt",
            data=st.session_state.response,
            file_name=f"legal_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col_b:
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            st.write("✅ Copied! (Select text and Ctrl+C)")

    with col_c:
        if st.button("👍 Helpful", use_container_width=True):
            with open("feedback.log", "a") as f:
                f.write(f"{datetime.now()}: Helpful\n")
            st.success("Thanks for your feedback!")

# ---------- FOOTER ----------
st.divider()
st.caption("⚖️ Legal AI Assistant — Built for contract analysis and legal summarization.")
